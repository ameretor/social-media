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
      results.forEach((result) => display_posts(result.content));
      results.forEach((result) => {
        console.log(
          "🚀 ~ file: post-comment.js ~ line 14 ~ .then ~ result",
          result
        );
      });
    });
}

function display_posts(post) {
  const control_post = document.createElement("div");
  control_post.id = "posts-design";
  control_post.innerHTML = `${post}`;
  document.querySelector("#posts").appendChild(control_post);
}
