document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views

  document
    .querySelector("#allPosts")
    .addEventListener("click", () => loadAllPosts());

  document
    .querySelector(".navbar-brand")
    .addEventListener("click", () => loadAllPosts());

  document
    .querySelector("#profile")
    .addEventListener("click", () => loadProfile());

  //TODO: Event listener for the Post button.  Update to go to function.
  document
    .querySelector("#post-button")
    .addEventListener("click", () => loadAllPosts());

  document
    .querySelector("#following")
    .addEventListener("click", () => loadFollowing());

  // By default, load the profile for the user
  loadProfile();
});

function loadAllPosts() {
  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "none";

  debugger;

  //TODO: Load all the existing posts.

  //TODO: Do not save if the post is empty?  Throw an error.

  //TODO: Clear out what is there after you Post it.

  //TODO: Add an event listener for the Post button.  Do it above.

  fetch(`/posts`)
    .then((response) => response.json())
    .then((posts) => {
      // Print email
      debugger;


      // TODO: this finally works!
      myJSONArray = JSON.parse(posts);
      test = myJSONArray[0]["content"]
      console.log(test)


      let counter = 0;

      for (let i = 0; i < myJSONArray.length; i++) {
        let obj = myJSONArray[i];
        sender2 = document.createElement("div");
        sender2.className = "inbox" + counter;

        document.querySelector("#allPostings").append(sender2);

        //create p within the div for
        sender3 = document.createElement("p");
        sender3.className = "left";
        sender3.innerHTML = obj.creator;
        console.log(obj.content);
        console.log(obj.creator);

        document.querySelector(".inbox" + counter).append(sender3);

        //create p within the div for the subject
        subject3 = document.createElement("p");
        subject3.className = "middle";
        subject3.innerHTML = obj.content;
        document.querySelector(".inbox" + counter).append(subject3);

        //create p within the div for the subject
        timestamp3 = document.createElement("p");
        timestamp3.className = "right";
        timestamp3.innerHTML = obj.createdDate;
        document.querySelector(".inbox" + counter).append(timestamp3);

        // Need to update stylesheet here.  Flag to mark email as read.

        counter++;
      }
    });

    // debugger;

    // document.querySelector(
    //   "#allPostings"
    // ).innerHTML = `<h4>You have no email in your Inbox.</h4>`;


}

function loadFollowing() {
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "block";
  document.querySelector("#profile-view").style.display = "none";

  fetch(`/following`)
    .then((response) => response.json())
    .then((following) => {
      // Print email
      console.log(following);
    });

  return false;
}

function loadProfile() {
  // debugger;
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "block";

  fetch(`/profile`)
    .then((response) => response.json())
    .then((profile) => {
      // Print email
      console.log(profile);
    });

  return false;
}
