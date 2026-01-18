document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-form").forEach(form => {
        form.addEventListener("submit", e => {
            e.preventDefault();

            const profileId = form.dataset.profileId;
            const csrfToken = form.querySelector(
                "input[name=csrfmiddlewaretoken]"
            ).value;

            fetch("/accounts/likes/toggle/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
                body: new URLSearchParams({
                    profile_id: profileId
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.liked) {
                    form.querySelector(".like-icon").src =
                        "/static/assets/icons/HeartOn.svg";
                } else {
                    form.querySelector(".like-icon").src =
                        "/static/assets/icons/HeartOff.svg";
                }
            });
        });
    });
});
