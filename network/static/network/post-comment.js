document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#posts").style.display = "flex";
  // Hide all comment-section elelements
  document.querySelectorAll(".comment-section").forEach((element) => {
    element.style.display = "block";
  });
  // Hide all commented elements
  document.querySelectorAll(".commented").forEach((element) => {
    element.style.display = "block";
  });
});

// Show comments section onclick
function showComments(postId) {
  document.querySelector(".comment-section-" + postId).style.display = "block";
  document.querySelector(".commented-" + postId).style.display = "block";
}

// Hide comments section onclick
function hideComments(postId) {
  document.querySelector(".comment-section-" + postId).style.display = "none";
  document.querySelector(".commented-" + postId).style.display = "none";
}
