document.addEventListener(
"DOMContentLoaded",
function(){


const elements =
document.querySelectorAll(
".animate, .fade-left, .fade-right"
);



const observer =
new IntersectionObserver(
(entries)=>{


entries.forEach(
(entry)=>{


if(entry.isIntersecting){

entry.target.classList.add(
"show"
);

}


});


},
{

threshold:0.15

}

);




elements.forEach(
(element)=>{

observer.observe(element);

});


});