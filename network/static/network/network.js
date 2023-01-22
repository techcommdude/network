document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views

  document.querySelector("#allPosts").addEventListener("click", () => loadAllPosts());

  document.querySelector(".navbar-brand").addEventListener("click", () => loadProfile());


  document.querySelector("#profile").addEventListener("click", () => loadProfile());

   //TODO: Event listener for the Post button.  Update to go to function.
   document
   .querySelector("#post-button")
   .addEventListener("click", () => loadProfile());

  // debugger;
  document
    .querySelector("#following")
    .addEventListener("click", () => loadFollowing());

  // By default, load the profile for the user
  loadProfile()
});

function loadAllPosts() {
  // debugger;

  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "none";

  //TODO: Load all the existing posts.

  //TODO: Do not save if the post is empty?  Throw an error.

  //TODO: Clear out what is there after you Post it.

  //TODO: Add an event listener for the Post button.  Do it above.
  return false;
}

function loadFollowing() {
  // debugger;
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "block";
  document.querySelector("#profile-view").style.display = "none";

  // return false;
}

function loadProfile() {
  // debugger;
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "block";

  // return false;
}
