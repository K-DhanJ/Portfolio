function startLoader() {
    let counterElement = document.querySelector(".counter");
    let overlay = document.querySelector(".overlay");
    let conteneur = document.querySelector(".conteneur");
    let currentValue = 0;

    // Bloquer le scrolling
    document.body.style.overflow = "hidden";

    function updateCounter() {
        if (currentValue >= 100) {
            return;
        }

        currentValue += Math.floor(Math.random() * 10) + 1;
        if (currentValue > 100) {
            currentValue = 100;
        }

        counterElement.textContent = currentValue;

        let delay = Math.floor(Math.random() * 200) + 50;
        setTimeout(updateCounter, delay);
    }
    updateCounter();

    // .black passe immédiatement à rgb(26, 26, 26)
    gsap.set(".black", { backgroundColor: "rgb(26, 26, 26)", zIndex: 3 });

    // Transition vers transparent en 1 seconde après 4.5 secondes
    gsap.to(".black", {
        backgroundColor: "transparent",
        duration: 1,
        delay: 4.5,
        onComplete: () => {
            document.querySelector(".black").style.zIndex = "0";
            document.body.style.overflow = "auto";
        }
    });

    gsap.to(".counter", 0.25, {
        delay: 3.5,
        opacity: 0,
        onComplete: () => {
            counterElement.style.display = "none";
        }
    });

    gsap.to(".bar", 1.5, {
        delay: 3.5,
        height: 0,
        stagger: {
            amount: 0.5,
        },
        ease: "power4.inOut",
    });

    gsap.from(".h1", 1.5, {
        delay: 4,
        y: 700,
        stagger: {
            amount: 0.5,
        },
        ease: "power4.inOut",
    });

    gsap.from(".herox", 2, {
        delay: 4.5,
        y: 400,
        ease: "power4.inOut",
    });

    // Ajout d'une transition en douceur via CSS
    overlay.style.transition = "opacity 0.5s ease-out";
    conteneur.style.transition = "opacity 0.5s ease-out";

    // Masquer .overlay et .conteneur après l'animation
    setTimeout(() => {
        overlay.style.opacity = "0";
        conteneur.style.opacity = "0";
    }, 4500);

    // Changer le z-index après 5 secondes (évite blocage)
    setTimeout(() => {
        overlay.style.zIndex = "0";
        conteneur.style.zIndex = "0";
        overlay.style.pointerEvents = "none";
        conteneur.style.pointerEvents = "none";
    }, 5000);
}

startLoader();
