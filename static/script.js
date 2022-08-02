const closeBtn = document.querySelector(".alert .btn-close");

// If there's an alert, allow it to be closed
// by clicking on the X button
if (closeBtn) {
    closeBtn.addEventListener("click", () => {
        const alertDiv = document.querySelector(".alert");
        alertDiv.remove();
    });
}

// Enable bootstrap tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})


const pageTitle = document.querySelector("title").textContent;

if (["Homepage", "About", "Login", "Register"].includes(pageTitle)) {
  const hrefValue = pageTitle === 'Homepage' ? '' : pageTitle.toLowerCase();
  const currentNavLink = document.querySelector(`.nav-link[href='/${hrefValue}']`);
  
  // Toggle nav-links active state
  document.querySelectorAll(".nav-link").forEach(link => {
    link.classList.remove("active");
    link.removeAttribute("aria-current");
  });
  currentNavLink.classList.add("active");
  currentNavLink.setAttribute("aria-current", "page");
}


// A function that stores the chosen theme
// in browser's localStorage
function switchTheme() {
  if (localStorage.getItem("currentTheme") === "light") {
    localStorage.setItem("currentTheme", "dark");
  } else {
    localStorage.setItem("currentTheme", "light");
  }

  location.reload();
}

const switchThemeBtn = document.querySelector(".switch-theme-btn");
switchThemeBtn.addEventListener("click", switchTheme);
switchThemeBtn.addEventListener("mouseover", () => {
  switchThemeBtn.src = switchThemeBtn.src.slice(0, -4) + "-fill" + ".svg";
});
switchThemeBtn.addEventListener("mouseout", () => {
  switchThemeBtn.src = switchThemeBtn.src.slice(0, -9) + ".svg";
});

if (!localStorage.getItem("currentTheme")) {
  localStorage.setItem("currentTheme", "light");
}

const navBar = document.querySelector(".navbar");
const allCards = document.querySelectorAll(".card");
const outlineBtns = document.querySelectorAll("[class*='btn-outline']");
const allInputFields = [...document.querySelectorAll("input"), ...document.querySelectorAll("textarea")];
const dropdownMenu = document.querySelector(".dropdown-menu");
const githubBtn = document.querySelector(".btn[href*='github']");
const modal = document.querySelector(".modal-content");

// A function that searches a string for a specified substring
// and returns the index where that substring starts
function findSubStr(str, subStr) {
  for (let i = 0; i < (str.length - subStr.length); i++) {
    if (str.slice(i, i + subStr.length) === subStr) {
      return i;
    }
  }

  return false;
}

// Change elements' background color and text color
// to match the chosen theme
if (localStorage.getItem("currentTheme") === "dark") {
  switchThemeBtn.src = "../static/images/sun.svg";

  document.body.classList.add("bg-dark");

  navBar.classList.remove("navbar-light");
  navBar.classList.add("navbar-dark");
  navBar.classList.add("bg-dark");
  navBar.classList.remove("bg-light");

  if (dropdownMenu) {
    dropdownMenu.classList.add("dropdown-menu-dark");
  };

  allCards.forEach(card => {
    card.classList.add("bg-dark");
    card.classList.add("text-light");
  });

  outlineBtns.forEach(btn => {
    let startIndex = findSubStr(btn.className, "outline");
    btn.className = btn.className.slice(0, startIndex) + btn.className.slice(startIndex + 8);
  });

  allInputFields.forEach(inputField => {
    inputField.classList.add("bg-dark");
    inputField.classList.add("text-light");
  });

  modal.classList.add("bg-dark");
  modal.classList.add("text-light");
  modal.querySelector(".btn-close").classList.add("bg-white");

  if (githubBtn) {
    githubBtn.classList.remove("btn-dark");
    githubBtn.classList.add("btn-outline-light");
  };
} else {
  switchThemeBtn.src = "../static/images/moon.svg";

  document.body.classList.remove("bg-dark");

  navBar.classList.add("navbar-light");
  navBar.classList.remove("navbar-dark");
  navBar.classList.remove("bg-dark");
  navBar.classList.add("bg-light");

  if (dropdownMenu) {
    dropdownMenu.classList.remove("dropdown-menu-dark");
  };

  allCards.forEach(card => {
    card.classList.remove("bg-dark");
    card.classList.remove("text-light");
  });

  outlineBtns.forEach(btn => {
    let startIndex = findSubStr(btn.className, "btn-")
    btn.className = btn.className.slice(0, startIndex + 4) + "outline-" + btn.className.slice(startIndex + 4 + 8);
  });

  allInputFields.forEach(inputField => {
    inputField.classList.remove("bg-dark");
    inputField.classList.remove("text-light");
  });

  modal.classList.remove("bg-dark");
  modal.classList.remove("text-light");
  modal.querySelector(".btn-close").classList.remove("bg-white");

  if (githubBtn) {
    githubBtn.classList.add("btn-dark");
    githubBtn.classList.remove("btn-outline-light");
  };
}
