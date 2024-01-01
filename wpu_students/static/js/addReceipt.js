const receiptBody = document.getElementById("receipt-body");
const addNewRowBtn = document.getElementById("add-row-btn");
const saveBtn = document.getElementById("save");
const [dateInput, notesInput, clientIdInput, clientNameInput, facultySelect] =
  document.querySelectorAll(":is(input, select)");
const totalDiv = document.getElementById("total");
const flashMessages = document.getElementById("flashed");

let data = {
  userId: receiptBody.getAttribute("data-user-id"),
  date: "",
  notes: "",
  id: "",
  clientName: "",
  faculty: "",
  rows: [],
};

// default values
let date = new Date();
date = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
dateInput.value = date;
data.date = date;
updateFacultySelect();

// event listeners
dateInput.addEventListener("change", () => (data.date = dateInput.value));
notesInput.addEventListener("change", () => (data.notes = notesInput.value));
clientIdInput.addEventListener("change", () => (data.id = clientIdInput.value));
clientNameInput.addEventListener("change", () => (data.clientName = clientNameInput.value));
facultySelect.addEventListener("change", () => updateFacultySelect());

clientIdInput.addEventListener("focus", () => {
  getClientInfo().then((clipboard) => {
    let id = (clipboard.match(/20[1-2]\d{6}/g) || [])[0];
    let name = (clipboard.match(/[^0-9\[\]]+/g) || [])[0];
    const criteria = !clientIdInput.value && !clientNameInput.value;
    if (id && criteria) {
      clientIdInput.value = id.trim();
      data.id = id;
    }
    if (name && id && criteria) {
      clientNameInput.value = name.trim();
      data.clientName = name.trim();
    }
  });
});

saveBtn.addEventListener("click", () => {
  fetch("/receipts/add", {
    body: JSON.stringify(data),
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => (res.status !== 201 ? res.json() : "ok"))
    .then((data) => {
      if (data === "ok") {
        location.reload();
      } else {
        flashMessages.innerHTML = "";
        const li = document.createElement("li");
        for (let err of data) {
          li.setAttribute("class", "alert alert-danger alert-dismissible fade show");
          li.setAttribute("role", "alert");
          const xBtn = document.createElement("button");
          xBtn.setAttribute("class", "btn-close");
          xBtn.setAttribute("type", "button");
          xBtn.setAttribute("data-bs-dismiss", "alert");
          xBtn.setAttribute("aria-label", "Close");
          li.innerHTML = err.loc + " " + err.msg;
          li.appendChild(xBtn);
        }
        flashMessages.appendChild(li);
      }
    });
});

addNewRowBtn.addEventListener("click", () => {
  fetch("/api/services")
    .then((res) => res.json())
    .then((options) => {
      let idx = data.rows.length ? data.rows[data.rows.length - 1].rowId + 1 : 1;

      // data manipulation
      data.rows.push({
        rowId: idx,
        serviceId: 0,
        qt: 0,
        price: 0,
        notes: "",
      });

      const rowTag = document.createElement("div");
      rowTag.setAttribute("class", "row g-1 align-middle mt-1");
      rowTag.setAttribute("data-id", idx);

      // dom manipulation
      const spanTag = document.createElement("span");
      spanTag.setAttribute("class", "d-flex justify-content-center align-items-center h-100");
      spanTag.innerHTML = rowTag.getAttribute("data-id");

      const rowIdx = idx;
      const selectTag = createSelectTag(options["result"]);
      const qtTag = createInputTag("number", false, 6, 1);
      const priceTag = createInputTag("number", false, 6, 0);
      const totalTag = createInputTag("text", true);
      const notesTag = createInputTag();

      // delete btn
      const deleteIcon = document.createElement("i");
      const deleteBtn = document.createElement("button");
      deleteBtn.setAttribute("class", "btn btn-danger btn-sm d-block w-100 h-100 rounded-2");
      deleteBtn.setAttribute("title", "Delete this row");
      deleteIcon.setAttribute("class", "fa-solid fa-trash");
      deleteBtn.addEventListener("click", () => {
        const criteria = confirm("Are sure you wanna DELETE this row?");
        if (criteria) {
          deleteBtn.parentElement.parentElement.remove();
          data.rows = data.rows.filter((e) => e.rowId !== rowIdx);
          calculateTotalDiv();
          idx--;
        }
      });
      deleteBtn.appendChild(deleteIcon);

      // add event listeners
      selectTag.addEventListener("change", () => updateSelectTag(selectTag, rowIdx));
      selectTag.addEventListener("focus", () => updateSelectTag(selectTag, rowIdx));
      selectTag.addEventListener("blur", () => updateSelectTag(selectTag, rowIdx));

      qtTag.addEventListener("change", () => updateQtPrice(qtTag, priceTag, totalTag, rowIdx));
      qtTag.addEventListener("focus", () => updateQtPrice(qtTag, priceTag, totalTag, rowIdx));
      qtTag.addEventListener("blur", () => updateQtPrice(qtTag, priceTag, totalTag, rowIdx));

      priceTag.addEventListener("change", () => updateQtPrice(qtTag, priceTag, totalTag, rowIdx));
      priceTag.addEventListener("focus", () => updateQtPrice(qtTag, priceTag, totalTag, rowIdx));
      priceTag.addEventListener("blur", () => updateQtPrice(qtTag, priceTag, totalTag, rowIdx));

      notesTag.addEventListener("change", () => updateNotes(notesTag, rowIdx));
      notesTag.addEventListener("focus", () => updateNotes(notesTag, rowIdx));
      notesTag.addEventListener("blur", () => updateNotes(notesTag, rowIdx));

      // creating column tag
      const tags = [
        createColTag(1, spanTag),
        createColTag(3, selectTag),
        createColTag(1, qtTag),
        createColTag(2, priceTag),
        createColTag(2, totalTag),
        createColTag(2, notesTag),
        createColTag(1, deleteBtn),
      ];

      for (let tag of tags) {
        rowTag.appendChild(tag);
      }

      receiptBody.appendChild(rowTag);
      if (receiptBody.children.length > 1) {
        selectTag.focus();
      } else {
        document.getElementsByName("date")[0].focus();
      }

      updateSelectTag(selectTag, idx);
      updateQtPrice(qtTag, priceTag, totalTag, idx);
    });
});

addNewRowBtn.click();

async function getClientInfo() {
  const data = await navigator.clipboard.readText();
  return data;
}

function updateFacultySelect() {
  let selectOptions = facultySelect.options;
  let selectedOptions = selectOptions[facultySelect.selectedIndex];
  let id = selectedOptions.getAttribute("value");
  data.faculty = +id;
}

function updateQtPrice(qtTag, priceTag, totalTag, idx) {
  let quantity = +qtTag.value;
  let price = +priceTag.value;
  calculateTotalTag(totalTag, quantity, price);
  let wantedData = data.rows.find((el) => el.rowId === idx);
  let rowIdx = data.rows.indexOf(wantedData);
  data.rows[rowIdx].qt = quantity;
  data.rows[rowIdx].price = price;
}

function updateNotes(notesTag, idx) {
  let wantedData = data.rows.find((el) => el.rowId === idx);
  let rowIdx = data.rows.indexOf(wantedData);
  data.rows[rowIdx].notes = notesTag.value;
}

function updateSelectTag(selectTag, idx) {
  let selectOptions = selectTag.options;
  let selectedOption = selectOptions[selectTag.selectedIndex];
  let id = selectedOption.getAttribute("value");
  let price = selectedOption.getAttribute("data-price");
  let totalTag = selectTag.parentElement.parentElement.querySelector("input[disabled]");
  selectTag.parentElement.parentElement.querySelector(
    "div:nth-child(4) > input[type='number']"
  ).value = +price;
  selectTag.parentElement.parentElement.querySelector(
    "div:nth-child(3) > input[type='number']"
  ).value = 1;
  let wantedData = data.rows.find((el) => el.rowId === idx);
  let rowIdx = data.rows.indexOf(wantedData);
  data.rows[rowIdx].serviceId = +id;
  data.rows[rowIdx].qt = 1;
  data.rows[rowIdx].price = +price;
  calculateTotalTag(totalTag, 1, price);
}

function calculateTotalTag(totalTag, qt, price) {
  let totalOfRow = qt * price;
  totalTag.value = totalOfRow.toLocaleString();
  calculateTotalDiv();
}

function calculateTotalDiv() {
  let total = data.rows.reduce((acc, el) => el.price * el.qt + acc, 0);
  totalDiv.innerHTML = `Total of receipt: <span class='text-body fw-bold'>${total.toLocaleString()}</span>`;
}

function createColTag(section, childTag) {
  const colTag = document.createElement("div");
  colTag.setAttribute("class", "col-" + section);
  colTag.appendChild(childTag);
  return colTag;
}

function createInputTag(type = "text", disabled = false, tabindex = 6, defaultValue = 0) {
  const inputTag = document.createElement("input");
  inputTag.setAttribute("type", type);
  inputTag.setAttribute("tabindex", tabindex);
  inputTag.setAttribute("value", 0);
  inputTag.setAttribute("name", "name");
  inputTag.setAttribute("autocomplete", "off");
  if (type === "number") {
    inputTag.setAttribute("value", defaultValue);
    inputTag.setAttribute("min", 1);
  } else {
    inputTag.setAttribute("value", "");
  }
  let classes = "form-control";
  if (disabled) {
    classes += " disabled";
    inputTag.setAttribute("disabled", "");
  }
  inputTag.setAttribute("class", classes);
  return inputTag;
}

function createSelectTag(options, tabindex = 6) {
  const selectTag = document.createElement("select");
  selectTag.setAttribute("class", "form-select");
  selectTag.setAttribute("tabindex", tabindex);
  selectTag.setAttribute("name", "name");
  selectTag.setAttribute("autocomplete", "on");
  for (let option of options) {
    let optionTag = document.createElement("option");
    optionTag.setAttribute("value", option.id);
    optionTag.setAttribute("data-price", option.price);
    optionTag.innerHTML = option.value;
    selectTag.appendChild(optionTag);
  }
  return selectTag;
}
