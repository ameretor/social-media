document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#posts").style.display = "flex";
  // Hide all all-about-comments elements
  document.querySelectorAll(".all-about-comments").forEach((element) => {
    element.style.display = "none";
  });

  showComments();
  showLikes();
});

// Show comments section on click comment-link element
function showComments() {
  document.querySelectorAll(".comment-link").forEach((element) => {
    // Listen for click event on comment-link element
    element.addEventListener("click", (event) => {
      // Get all-about-comments element by data-postid attribute
      const allAboutComments = document.querySelector(
        `.all-about-comments[data-postid="${event.target.dataset.postid}"]`
      );
      if (allAboutComments.style.display === "block") {
        allAboutComments.style.display = "none";
        document.querySelector(
          `.comment-link[data-postid="${event.target.dataset.postid}"]`
        ).innerHTML = "Comments";
      } else {
        allAboutComments.style.display = "block";
        document.querySelector(
          `.comment-link[data-postid="${event.target.dataset.postid}"]`
        ).innerHTML = "Hide comments";
      }
    });
  });
}
