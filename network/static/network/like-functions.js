// document.addEventListener("DOMContentLoaded", () => {
//   showLikes();
// });

// function showLikes() {
//   // Hide all thumbs-up-filled elements
//   document.querySelectorAll(".thumbs-up-button").forEach((element) => {
//     element.style.display = "block";
//   });
//   document.querySelectorAll(".thumbs-up-filled").forEach((element) => {
//     element.style.display = "none";
//   });
//   //   Show thumbs-up-filled when thumbs-up-button is clicked and vice versa
//   document.querySelectorAll(".thumbs-up-button").forEach((element) => {
//     element.addEventListener("click", () => {
//       element.style.display = "none";
//       element.nextElementSibling.style.display = "block";
//     });
//   });
//   document.querySelectorAll(".thumbs-up-filled").forEach((element) => {
//     element.addEventListener("click", () => {
//       element.style.display = "none";
//       element.previousElementSibling.style.display = "block";
//     });
//   });
// }
