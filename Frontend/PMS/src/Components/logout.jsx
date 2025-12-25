function handleLogout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");

  // works anywhere, no React dependency
  window.location.replace("/signup");
}

export default handleLogout;
