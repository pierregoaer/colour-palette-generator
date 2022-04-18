// ----- Copy HEX code to clipboard -----

const hexCodeCopyButtons = document.querySelectorAll(".copy-hex-code")

hexCodeCopyButtons.forEach( button =>
		(button.onclick = () => {
		    hexCode = button.dataset.colour;
		    console.log(hexCode);
		     navigator.clipboard.writeText(hexCode)
		})

)


// ----- Change number of colours on slider input -----
const coloursSlider = document.querySelector(".num-colours-slider")
const output = document.querySelector(".slider-output");

coloursSlider.oninput = function() {
    suffix = this.value == 1 ? " colour" :" colours"
    text = this.value + suffix
    output.innerHTML = text;
}