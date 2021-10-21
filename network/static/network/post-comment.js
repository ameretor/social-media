document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#posts").style.display = "block";
  posting("post");
  console.log("Fuck all");
});

function posting(action) {
  fetch(`load_posts/${action}`)
    .then((response) => response.json())
    .then((results) => {
      console.log("good");
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
  const control_post = document.createElement("div");
  control_post.id = "posts-design";

  const post_content = document.createElement("div");
  post_content.id = "post-content";

  post_content.innerHTML = `${content}`;
  control_post.appendChild(post_content);
  document.querySelector("#posts").appendChild(control_post);
}
