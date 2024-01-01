const editableModalBtns = document.querySelectorAll(".editable-modal-btn");
const editableModal = document.querySelector(".editable-modal");

editableModalBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    let data = btn.getAttribute("data-data");
    data = JSON.parse(data);
    const modalTitle = editableModal.querySelector(".modal-title");
    const modalSubmitBtn = editableModal.querySelector("button[type='submit']");
    const modalForm = editableModal.querySelector("form");
    let modalFormAction = modalForm.getAttribute("action");

    modalFormAction = modalFormAction.replace(/\d+/g, `${data.id}`);
    modalTitle.innerHTML = "Edit " + data.modalTitle;
    modalSubmitBtn.innerHTML = "Edit " + data.modalTitle;
    modalForm.setAttribute("action", modalFormAction);

    const inputs = modalForm.querySelectorAll("input");

    if (inputs.length === data.values.length) {
      for (let i = 0; i < inputs.length; i++) {
        inputs[i].setAttribute("value", data.values[i]);
      }
    }
  });
});
