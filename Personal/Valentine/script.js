
let currentMode = "cute";
let soundEnabled = true;

window.onload = () => {
const saved = localStorage.getItem("theme");
if(saved){
document.body.classList.add(saved);
}else{
if(window.matchMedia("(prefers-color-scheme: dark)").matches){
document.body.classList.add("dark");
}else{
document.body.classList.add("light");
}
}
updateLeaderboard();
};

function toggleTheme(){
if(document.body.classList.contains("light")){
document.body.classList.replace("light","dark");
localStorage.setItem("theme","dark");
}else{
document.body.classList.replace("dark","light");
localStorage.setItem("theme","light");
}
}

function toggleSound(){
soundEnabled=!soundEnabled;
document.getElementById("soundBtn").innerText = soundEnabled ? "🔊":"🔇";
}

function changeMode(){
currentMode=document.getElementById("modeSelect").value;
}

async function generateMessage(){
const output=document.getElementById("output");
output.innerText="Generating magic... ✨";

let promptMap={
cute:"Write a cute playful romantic Valentine message under 40 words.",
dramatic:"Write a dramatic cinematic love confession under 40 words.",
chaotic:"Write a funny chaotic meme-style Valentine message under 40 words.",
mysterious:"Write a mysterious poetic love message under 40 words."
};

try{
const response=await fetch("https://llama3.protosonline.in/v1/chat/completions",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
model:"llama3",
messages:[
{role:"system",content:"You are a creative romantic assistant."},
{role:"user",content:promptMap[currentMode]}
],
temperature:0.9,
max_tokens:80
})
});

const data=await response.json();

const text = data.choices?.[0]?.message?.content || "Love is loading...";
const cleaned = text
  .replace(/^"+|"+$/g, "")      // remove wrapping quotes
  .replace(/\n+/g, " ")         // remove excessive line breaks
  .trim();

typeWriter(cleaned);

}catch(e){
output.innerText="AI is shy today 😅";
}
}

function typeWriter(text){
const output=document.getElementById("output");
output.innerText="";
let i=0;
let interval=setInterval(()=>{
output.innerText+=text.charAt(i);
i++;
if(i>=text.length) clearInterval(interval);
},25);
}

function celebrate(){
launchConfetti();
saveYes();
if(soundEnabled) new Audio("https://assets.mixkit.co/sfx/preview/mixkit-achievement-bell-600.mp3").play();
}

function moveNo(){
const btn=document.getElementById("noBtn");
btn.style.position="absolute";
btn.style.left=Math.random()*window.innerWidth+"px";
btn.style.top=Math.random()*window.innerHeight+"px";
}

function launchConfetti(){
const canvas=document.getElementById("confetti");
const ctx=canvas.getContext("2d");
canvas.width=window.innerWidth;
canvas.height=window.innerHeight;

let pieces=Array.from({length:120},()=>({x:Math.random()*canvas.width,y:Math.random()*canvas.height,r:Math.random()*6+4}));

function draw(){
ctx.clearRect(0,0,canvas.width,canvas.height);
ctx.fillStyle="pink";
pieces.forEach(p=>{
ctx.beginPath();
ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
ctx.fill();
p.y+=3;
if(p.y>canvas.height)p.y=0;
});
}
setInterval(draw,20);
}

function downloadScreenshot(){
html2canvas(document.body).then(canvas=>{
const link=document.createElement("a");
link.download="valentine.png";
link.href=canvas.toDataURL();
link.click();
});
}

function shareLink(){
const url=window.location.origin + window.location.pathname + "?mode="+currentMode;
navigator.clipboard.writeText(url);
alert("Share link copied! 💘");
}

function saveYes(){
let count=localStorage.getItem("yesCount")||0;
count++;
localStorage.setItem("yesCount",count);
updateLeaderboard();
}

function updateLeaderboard(){
let count=localStorage.getItem("yesCount")||0;
document.getElementById("leaderboard").innerText="YES clicks: "+count;
}
