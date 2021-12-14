document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".posts").forEach((element) => {
    showModalEditPost(element);
    deletePost(element);
  });
});
