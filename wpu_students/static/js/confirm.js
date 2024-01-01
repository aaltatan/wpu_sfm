const btns = document.querySelectorAll(".confirm");

btns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    let message = btn.getAttribute("data-msg");
    let conf = confirm(message);
    if (!conf) {
      e.preventDefault();
    }
  });
});
