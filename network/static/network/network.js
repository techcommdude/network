document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views

  //FIXME:

  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));

  //This is the Sent button at the top of the page.
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));

  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));

  //Listener on the Compose button at the top of the page.
  document.querySelector("#compose").addEventListener("click", compose_email);

  // Send Mail: When a user submits the email composition form.  Prevent default is needed to prevent the inbox from loading by default.
  //This is the listener on the form.
  document
    .querySelector("#compose-form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      submit_email();
    });

  // By default, load the inbox
  // load_mailbox("inbox");
});
