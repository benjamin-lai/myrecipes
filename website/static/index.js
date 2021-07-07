function createComment2(recipe_id) {
  var new_comment = prompt("Create a new comment on this recipe.");
  if (new_comment != null) {
    fetch("/create-comment", {
      method: "POST",
      body: JSON.stringify({
        recipe_id: recipe_id,
        comment: new_comment,
      }),
    }).then((_res) => {
      window.location.reload(true);
    });
  }
}

function deleteComment(comment_id) {
  fetch("/delete-comment", {
    method: "POST",
    body: JSON.stringify({ comment_id: comment_id }),
  }).then((_res) => {
    window.location.reload(true);
  });
}

function modifyComment(comment_id) {
  var new_comment = prompt("Enter new comment to change.");
  if (new_comment != null) {
    fetch("/modify-comment", {
      method: "POST",
      body: JSON.stringify({ comment_id: comment_id, comment: new_comment }),
    }).then((_res) => {
      window.location.reload(true);
    });
  }
}

function addLike(recipe_id) {
  fetch("/add-like", {
    method: "POST",
    body: JSON.stringify({ recipe_id: recipe_id }),
  }).then((_res) => {
    window.location.reload(true);
  });
}

function addDislike(recipe_id) {
  fetch("/add-dislike", {
    method: "POST",
    body: JSON.stringify({ recipe_id: recipe_id }),
  }).then((_res) => {
    window.location.reload(true);
  });
}
