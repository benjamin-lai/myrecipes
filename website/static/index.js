function deleteComment(comment_id) {
  fetch("/delete-comment", {
    method: "POST",
    body: JSON.stringify({ comment_id: comment_id }),
  }).then((_res) => {
    window.location.reload(true);
  });
}
