const aside = document.getElementById("aside");
const asideOpenBtn = document.getElementById("aside-open-btn");
asideOpenBtn.addEventListener("click", () => {
  aside.classList.toggle("closed");
});
