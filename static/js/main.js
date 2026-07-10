console.log("Sensation.Tech Loaded Successfully");
const iris=document.querySelector(".iris");

document.addEventListener("mousemove",(e)=>{

if(!iris) return;

let x=(e.clientX/window.innerWidth-.5)*40;

let y=(e.clientY/window.innerHeight-.5)*40;

iris.style.transform=`translate(${x}px,${y}px)`;

});
