document.addEventListener("DOMContentLoaded", function () {
    function updateNotifications() {
        fetch('/get_notifications/')
            .then(response => response.json())
            .then(data => {
                const notificationCount = document.getElementById("notificationCount");
                const notificationMenu = document.getElementById("notificationMenu");

                if (data.length > 0) {
                    notificationCount.innerText = data.length;
                    notificationMenu.innerHTML = "";
                    data.forEach(notif => {
                        let item = document.createElement("li");
                        item.className = "dropdown-item";
                        item.innerText = notif.message;
                        notificationMenu.appendChild(item);
                    });
                } else {
                    notificationCount.innerText = "0";
                    notificationMenu.innerHTML = "<li class='dropdown-item'>No new notifications</li>";
                }
            });
    }

    setInterval(updateNotifications, 10000); // Refresh every 10 seconds
});
