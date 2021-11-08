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
  show_comments();
});

function posting(action) {
  fetch(`load_posts/${action}`)
    .then((response) => response.json())
    .then((results) => {
      console.log(results);
      results.forEach((result) => display_posts_contents(result.content));
      results.forEach((result) => {
        console.log(
          "🚀 ~ file: post-comment.js ~ line 14 ~ .then ~ result",
          result
        );
      });
    });
}

function display_posts_contents(content) {
  // Create control elements
  const control_post = document.createElement("div");
  control_post.id = "posts-design";
  // Create posts contents elements
  const post_content = document.createElement("div");
  post_content.id = "post-content";
  post_content.innerHTML = `Javascript ${content}`;
  control_post.appendChild(post_content);
  document.querySelector("#posts").appendChild(control_post);
  // Create comments link
  const comment_link = document.createElement("div");
  comment_link.id = "comment-link";
  comment_link.innerHTML = "Comments";
  control_post.appendChild(comment_link);
}

// Show commented elements base on data-postId
function show_comments() {
  document.querySelectorAll(".comment-link").forEach((element) => {
    element.addEventListener("click", (event) => {
      const post_id = event.target.parentElement.parentElement.dataset.postid;
      console.log(post_id);
      fetch(`load_comments/${post_id}`)
        .then((response) => response.json())
        .then((results) => {
          console.log(results);
          results.forEach((result) =>
            display_comments_contents(result.content)
          );
          results.forEach((result) => {
            console.log(
              "🚀 ~ file: post-comment.js ~ line 41 ~ .then ~ result",
              result
            );
          });
        });
    });
  });
}
