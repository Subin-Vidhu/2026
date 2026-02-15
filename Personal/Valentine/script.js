
let currentStep = 1;
let rainActive = false;
let rainInterval;
let rainSoundActive = false;

function goToStep(step){
document.getElementById("step"+currentStep).classList.remove("active");
currentStep = step;
document.getElementById("step"+currentStep).classList.add("active");
}

function toggleTheme(){
document.body.classList.toggle("dark");
}

async function generateMessage(){
const name = document.getElementById("nameInput").value || "someone special";
const mode = document.getElementById("modeSelect").value;
const output = document.getElementById("output");

const prompts = {
college:`Write a nostalgic Kerala-style college romantic message for ${name} under 50 words.`,
cinematic:`Write a deep emotional cinematic love confession for ${name} under 50 words.`,
urban:`Write a modern urban romantic message set in Kerala for ${name}.`,
poetic:`Write a short poetic romantic message for ${name}.`
};

output.innerText = "Writing magic... ✨";

try{
const res = await fetch("https://llama3.protosonline.in/v1/chat/completions",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
model:"llama3",
messages:[
{role:"system",content:"You are a creative romantic writer inspired by Kerala monsoon evenings."},
{role:"user",content:prompts[mode]}
],
temperature:0.9,
max_tokens:100
})
});

const data = await res.json();
const text = data.choices?.[0]?.message?.content || "Love loading...";
output.innerText = text.replace(/^"+|"+$/g,"");
}catch(e){
output.innerText = "AI is shy today 😅";
}
}

function celebrate(){
launchConfetti();
saveYes();
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

function toggleRain(){
rainActive=!rainActive;
if(rainActive) startRain();
else stopRain();
}

function startRain(){
const canvas=document.getElementById("rain");
const ctx=canvas.getContext("2d");
canvas.width=window.innerWidth;
canvas.height=window.innerHeight;

let drops=Array.from({length:300},()=>({x:Math.random()*canvas.width,y:Math.random()*canvas.height,length:Math.random()*20+10,speed:Math.random()*5+5}));

rainInterval=setInterval(()=>{
ctx.clearRect(0,0,canvas.width,canvas.height);
ctx.strokeStyle="rgba(173,216,230,0.5)";
ctx.lineWidth=1;

drops.forEach(d=>{
ctx.beginPath();
ctx.moveTo(d.x,d.y);
ctx.lineTo(d.x,d.y+d.length);
ctx.stroke();
d.y+=d.speed;
if(d.y>canvas.height){d.y=-20;d.x=Math.random()*canvas.width;}
});
},30);

setInterval(()=>{
if(Math.random()>0.85){
document.body.classList.add("lightning");
setTimeout(()=>{document.body.classList.remove("lightning");},200);
}
},5000);
}

function stopRain(){
clearInterval(rainInterval);
const canvas=document.getElementById("rain");
const ctx=canvas.getContext("2d");
ctx.clearRect(0,0,canvas.width,canvas.height);
}

function toggleRainSound(){
const audio=document.getElementById("rainAudio");
rainSoundActive=!rainSoundActive;
if(rainSoundActive) audio.play();
else audio.pause();
}

function downloadScreenshot(){
html2canvas(document.body).then(canvas=>{
const link=document.createElement("a");
link.download="ente-valentine.png";
link.href=canvas.toDataURL();
link.click();
});
}

function generateShare(){
const name=document.getElementById("nameInput").value||"";
const mode=document.getElementById("modeSelect").value;
const url=window.location.origin+window.location.pathname+"?name="+encodeURIComponent(name)+"&mode="+mode;
navigator.clipboard.writeText(url);
alert("Share link copied! 💘");
}

function saveYes(){
let count=localStorage.getItem("yesCount")||0;
count++;
localStorage.setItem("yesCount",count);
document.getElementById("leaderboard").innerText="YES clicks: "+count;
}
