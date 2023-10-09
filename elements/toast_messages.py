
import streamlit.components.v1 as components
_ = components.html(
"""
<script>
function loadScript(url)
{       

return new Promise(function(resolve, reject) {

    //Add the script to the main page, not the component iframe
    const doc = window.parent.document;

    var head = doc.getElementsByTagName('head')[0];
    var script = doc.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    script.async = false
    script.onreadystatechange = resolve;
    script.onload = resolve;
    // Fire the loading
    head.appendChild(script);
});
}
function loadCSS(url)
{       
return new Promise(function(resolve, reject) {
    // Same thing about the main page
    const doc = window.parent.document;
    var head = doc.getElementsByTagName('head')[0];
    let cssLink = doc.createElement("link");
    cssLink.setAttribute("rel", "stylesheet");
    cssLink.setAttribute("type", "text/css");
    cssLink.setAttribute("href", url);
    cssLink.onreadystatechange = resolve;
    cssLink.onload = resolve;
    head.appendChild(cssLink);
});
}

loadScript('https://cdn.jsdelivr.net/npm/toastify-js').then( () => {
console.log('Script loaded')
loadCSS("https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css").then( () => {
    console.log('CSS Loaded')
    // Prefix the Toastify object with `parent.` since we are in the iframe
    parent.Toastify({
        text: "This is a test toast",
        duration: 3000,
        destination: "https://github.com/apvarun/toastify-js",
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        
    }).showToast();
})
})

</script>
""",
height=0,
width=0,
)




