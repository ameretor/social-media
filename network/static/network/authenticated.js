document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".posts").forEach((postNode) => {
    editPostManager(postNode);
    let csrf = getCookie("csrftoken");
    console.log(csrf);
  });
});
