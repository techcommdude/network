document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views

  document.querySelector("#allPosts").addEventListener("click", () => loadAllPosts());

  document.querySelector(".navbar-brand").addEventListener("click", () => profile());


  document.querySelector("#profile").addEventListener("click", () => profile());

   //TODO: Event listener for the Post button.  Update to go to function.
   document
   .querySelector("#post-button")
   .addEventListener("click", () => profile());

  // debugger;
  document
    .querySelector("#following")
    .addEventListener("click", () => following());

  // By default, load the profile for the user
  profile()
});

function loadAllPosts() {
  // debugger;

  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "none";

  //TODO: Load all the existing posts.

  //TODO: Add an event listener for the Post button.  Do it above.
  return false;
}

function following() {
  // debugger;
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "block";
  document.querySelector("#profile-view").style.display = "none";

  // return false;
}

function profile() {
  // debugger;
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "block";

  // return false;
}
