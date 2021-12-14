function showModalEditPost(post) {
  let postId = post.dataset.postid;
  let editButtn = document.getElementById(`edit_${post.dataset.postid}`);
  modal = document.getElementById(`myModal`);
  clseBttn = document.getElementsByClassName("close")[0];
  let modalBody = modal.querySelector(".modal-body");
  let saveBtn = document.querySelector(".saveBtn");

  // On click edit button
  editButtn.onclick = function () {
    console.log(`Post edited at ${postId}`);
    modal.style.display = "block";
    let postContent = document.querySelector(
      `.post-content[data-postid='${post.dataset.postid}']`
    );
    const contentInnerText = postContent.innerText;
    modalBody.innerHTML = `<textarea class="new-content form-control">${contentInnerText}</textarea>`;

    saveBtn.addEventListener("click", () => {
      const submittedContent = modalBody.querySelector(".new-content").value;

      let csrftoken = getCookie("csrftoken");

      // Send PUT request
      fetch(`post-comment/post`, {
        method: "PUT",
        body: JSON.stringify({
          id: postId,
          content: submittedContent,
        }),
        headers: { "X-CSRFToken": csrftoken },
      })
        .then((response) => {
          // Get response
          postContent.innerHTML = submittedContent;
          console.log(`Post content updated at ${postId}`);
          let response_body = response.json;

          throw new Error(response_body.error);
        })
        .catch((err) => {
          console.error(err);
        });
      window.location.reload();
      modal.style.display = "none";
    });
  };

  clseBttn.onclick = function () {
    modal.style.display = "none";
  };
  window.onclick = function (e) {
    if (e.target == modal) {
      modal.style.display = "none";
    }
  };

  // grab post content and put in text area
}

function deletePost(post) {
  let postId = post.dataset.postid;
  delBtn = document.getElementById(`delete_${post.dataset.postid}`);

  // On click delete button
  delBtn.onclick = function () {
    let csrftoken = getCookie("csrftoken");
    // Send DELETE request
    fetch(`post-comment/post`, {
      method: "DELETE",
      body: JSON.stringify({
        id: postId,
      }),
      headers: { "X-CSRFToken": csrftoken },
    })
      .then((response) => {
        // Get response
        console.log(`Post deleted at ${postId}`);
        let response_body = response.json;
        throw new Error(response_body.error);
      })
      .catch((err) => {
        console.error(err);
      });
    window.location.reload();
  };
}
