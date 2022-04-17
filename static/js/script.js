const hexCodeCopyButtons = document.querySelectorAll(".copy-hex-code")

hexCodeCopyButtons.forEach( button =>
		(button.onclick = () => {
		    hexCode = button.dataset.colour;
		    console.log(hexCode);
		     navigator.clipboard.writeText(hexCode)
		})

)