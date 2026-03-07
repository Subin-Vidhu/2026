(() => {
  const canvas = document.getElementById("weather-canvas");
  const ctx = canvas.getContext("2d", { alpha: true });

  const weatherSelect = document.getElementById("weather-select");
  const intensityInput = document.getElementById("intensity");
  const windInput = document.getElementById("wind");
  const soundToggle = document.getElementById("sound-toggle");
  const dayNightToggle = document.getElementById("day-night-toggle");
  const intensityValue = document.getElementById("intensity-value");
  const windValue = document.getElementById("wind-value");
  const icon = document.getElementById("weather-icon");
  const flashOverlay = document.getElementById("flash-overlay");

  const state = {
    weather: "rain",
    intensity: 55,
    wind: 35,
    isDay: true,
    soundOn: true,
    lightningAlpha: 0,
    lightningTimer: 0,
    width: window.innerWidth,
    height: window.innerHeight,
  };

  const particles = [];
  const clouds = [];
  const birds = [];

  const audio = createAudioEngine();

  function createAudioEngine() {
    let context = null;
    let masterGain = null;
    let noiseSource = null;
    let weatherGain = null;
    let toneOsc = null;
    let toneGain = null;

    function ensureContext() {
      if (context) return;
      context = new (window.AudioContext || window.webkitAudioContext)();
      masterGain = context.createGain();
      masterGain.gain.value = 0.28;
      masterGain.connect(context.destination);
    }

    function stopCurrent() {
      if (noiseSource) {
        noiseSource.stop();
        noiseSource.disconnect();
        noiseSource = null;
      }
      if (weatherGain) {
        weatherGain.disconnect();
        weatherGain = null;
      }
      if (toneOsc) {
        toneOsc.stop();
        toneOsc.disconnect();
        toneOsc = null;
      }
      if (toneGain) {
        toneGain.disconnect();
        toneGain = null;
      }
    }

    function createNoiseLoop(filterType, freq, gainLevel, playbackRate = 1, qValue = 0.8) {
      const bufferSize = Math.floor(context.sampleRate * 0.35);
      const buffer = context.createBuffer(1, bufferSize, context.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i += 1) {
        data[i] = Math.random() * 2 - 1;
      }

      const source = context.createBufferSource();
      source.buffer = buffer;
      source.loop = true;
      source.playbackRate.value = playbackRate;

      const filter = context.createBiquadFilter();
      filter.type = filterType;
      filter.frequency.value = freq;
      filter.Q.value = qValue;

      const gain = context.createGain();
      gain.gain.value = gainLevel;

      source.connect(filter);
      filter.connect(gain);
      gain.connect(masterGain);
      source.start();

      noiseSource = source;
      weatherGain = gain;
    }

    function play(mode, intensity) {
      if (!state.soundOn) return;
      ensureContext();
      if (context.state === "suspended") {
        context.resume();
      }
      stopCurrent();

      const normalized = intensity / 100;

      if (mode === "rain") {
        createNoiseLoop("highpass", 950, 0.1 + normalized * 0.12, 1.9, 0.45);
      } else if (mode === "snow") {
        createNoiseLoop("bandpass", 780, 0.05 + normalized * 0.06, 1.35, 0.95);

        toneOsc = context.createOscillator();
        toneGain = context.createGain();
        toneOsc.type = "sine";
        toneOsc.frequency.value = 230 + normalized * 80;
        toneGain.gain.value = 0.008 + normalized * 0.012;
        toneOsc.connect(toneGain);
        toneGain.connect(masterGain);
        toneOsc.start();
      } else {
        toneOsc = context.createOscillator();
        toneGain = context.createGain();
        toneOsc.type = "triangle";
        toneOsc.frequency.value = 460 + normalized * 130;
        toneGain.gain.value = 0.008 + normalized * 0.01;
        toneOsc.connect(toneGain);
        toneGain.connect(masterGain);
        toneOsc.start();
      }
    }

    function setEnabled(enabled) {
      state.soundOn = enabled;
      if (!enabled) {
        stopCurrent();
      } else {
        play(state.weather, state.intensity);
      }
    }

    return { play, setEnabled };
  }

  function resize() {
    state.width = window.innerWidth;
    state.height = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(state.width * dpr);
    canvas.height = Math.floor(state.height * dpr);
    canvas.style.width = `${state.width}px`;
    canvas.style.height = `${state.height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function random(min, max) {
    return min + Math.random() * (max - min);
  }

  function spawnParticles(targetCount) {
    while (particles.length < targetCount) {
      if (state.weather === "rain") {
        particles.push({
          x: random(0, state.width),
          y: random(-state.height, state.height),
          len: random(8, 22),
          speed: random(380, 630),
          thickness: random(1, 2.2),
        });
      } else if (state.weather === "snow") {
        particles.push({
          x: random(0, state.width),
          y: random(-state.height, state.height),
          radius: random(1.8, 4.8),
          speed: random(18, 58),
          wobble: random(0, Math.PI * 2),
          drift: random(0.2, 1),
        });
      }
    }
    if (particles.length > targetCount) {
      particles.length = targetCount;
    }
  }

  function ensureSunObjects() {
    if (state.weather !== "sun") {
      clouds.length = 0;
      birds.length = 0;
      return;
    }

    if (clouds.length === 0) {
      for (let i = 0; i < 6; i += 1) {
        clouds.push({
          x: random(-140, state.width),
          y: random(30, state.height * 0.45),
          size: random(34, 82),
          speed: random(10, 28),
        });
      }
    }
  }

  function updateParticles(dt) {
    const intensityFactor = state.intensity / 100;
    const windForce = (state.wind / 100) * (state.weather === "rain" ? 100 : 45);

    if (state.weather === "rain") {
      const count = Math.floor(80 + intensityFactor * 460);
      spawnParticles(count);
      ctx.strokeStyle = state.isDay ? "rgba(118,190,255,0.9)" : "rgba(133,179,255,0.8)";

      for (const p of particles) {
        p.y += p.speed * dt;
        p.x += windForce * dt;

        if (p.y > state.height + 25 || p.x > state.width + 20) {
          p.y = random(-120, -10);
          p.x = random(-30, state.width * 0.9);
        }

        ctx.lineWidth = p.thickness;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x - windForce * 0.03, p.y + p.len);
        ctx.stroke();
      }

      state.lightningTimer -= dt;
      if (state.lightningTimer <= 0 && Math.random() < 0.009 + intensityFactor * 0.03) {
        state.lightningAlpha = 0.9;
        state.lightningTimer = random(1.8, 5.5);
      }
      state.lightningAlpha = Math.max(0, state.lightningAlpha - dt * 3);
      flashOverlay.style.opacity = state.lightningAlpha.toFixed(3);
    } else if (state.weather === "snow") {
      const count = Math.floor(45 + intensityFactor * 330);
      spawnParticles(count);

      for (const p of particles) {
        p.wobble += dt;
        p.y += p.speed * dt;
        p.x += Math.sin(p.wobble * p.drift * 3) * (14 + windForce * 0.2) * dt + windForce * dt * 0.45;

        if (p.y > state.height + 8) {
          p.y = -10;
          p.x = random(-40, state.width + 40);
        }
        if (p.x > state.width + 40) p.x = -20;
        if (p.x < -40) p.x = state.width + 20;

        ctx.fillStyle = state.isDay ? "rgba(255,255,255,0.95)" : "rgba(228,240,255,0.9)";
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();
      }
      flashOverlay.style.opacity = "0";
    } else {
      particles.length = 0;
      flashOverlay.style.opacity = "0";
    }
  }

  function updateSunScene(dt) {
    if (state.weather !== "sun") return;

    const windBoost = state.wind / 100;

    for (const cloud of clouds) {
      cloud.x += (cloud.speed + windBoost * 28) * dt;
      if (cloud.x - cloud.size * 2 > state.width) {
        cloud.x = -cloud.size * 2;
        cloud.y = random(30, state.height * 0.45);
      }

      ctx.fillStyle = state.isDay ? "rgba(255,255,255,0.82)" : "rgba(214,228,255,0.5)";
      drawCloud(cloud.x, cloud.y, cloud.size);
    }

    if (Math.random() < 0.008) {
      birds.push({
        x: -80,
        y: random(35, state.height * 0.45),
        speed: random(90, 170),
        wing: random(0, Math.PI * 2),
        scale: random(0.8, 1.4),
      });
    }

    for (let i = birds.length - 1; i >= 0; i -= 1) {
      const b = birds[i];
      b.x += b.speed * dt;
      b.wing += dt * 9;
      drawBird(b);
      if (b.x > state.width + 120) birds.splice(i, 1);
    }
  }

  function drawCloud(x, y, size) {
    ctx.beginPath();
    ctx.arc(x, y, size * 0.35, Math.PI * 0.5, Math.PI * 1.5);
    ctx.arc(x + size * 0.35, y - size * 0.22, size * 0.28, Math.PI, Math.PI * 2);
    ctx.arc(x + size * 0.72, y - size * 0.05, size * 0.32, Math.PI * 1.15, Math.PI * 1.95);
    ctx.arc(x + size, y, size * 0.25, Math.PI * 1.4, Math.PI * 0.6);
    ctx.closePath();
    ctx.fill();
  }

  function drawBird(bird) {
    const flap = Math.sin(bird.wing) * 6 * bird.scale;
    ctx.strokeStyle = state.isDay ? "rgba(45,55,78,0.8)" : "rgba(220,228,248,0.75)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(bird.x, bird.y);
    ctx.quadraticCurveTo(bird.x + 9 * bird.scale, bird.y - flap, bird.x + 18 * bird.scale, bird.y);
    ctx.quadraticCurveTo(bird.x + 27 * bird.scale, bird.y - flap, bird.x + 36 * bird.scale, bird.y);
    ctx.stroke();
  }

  function applyUIClasses() {
    document.body.classList.remove("weather-rain", "weather-snow", "weather-sun");
    document.body.classList.add(`weather-${state.weather}`);

    document.body.classList.toggle("day", state.isDay);
    document.body.classList.toggle("night", !state.isDay);

    icon.classList.remove("rain", "snow", "sun");
    icon.classList.add(state.weather);
    icon.style.transform = "scale(0.9)";
    requestAnimationFrame(() => {
      icon.style.transform = "scale(1)";
    });

    icon.setAttribute("aria-label", `${state.weather[0].toUpperCase()}${state.weather.slice(1)} weather icon`);
  }

  function syncLabels() {
    intensityValue.textContent = String(state.intensity);
    windValue.textContent = String(state.wind);
  }

  function onWeatherChange() {
    particles.length = 0;
    clouds.length = 0;
    birds.length = 0;
    state.lightningAlpha = 0;
    state.lightningTimer = random(1.5, 4.5);
    applyUIClasses();
    ensureSunObjects();
    audio.play(state.weather, state.intensity);
  }

  weatherSelect.addEventListener("change", (event) => {
    state.weather = event.target.value;
    onWeatherChange();
  });

  intensityInput.addEventListener("input", (event) => {
    state.intensity = Number(event.target.value);
    syncLabels();
    audio.play(state.weather, state.intensity);
  });

  windInput.addEventListener("input", (event) => {
    state.wind = Number(event.target.value);
    syncLabels();
  });

  soundToggle.addEventListener("change", (event) => {
    audio.setEnabled(event.target.checked);
  });

  dayNightToggle.addEventListener("change", (event) => {
    state.isDay = event.target.checked;
    const label = event.target.nextElementSibling;
    label.textContent = state.isDay ? "Day Mode" : "Night Mode";
    applyUIClasses();
  });

  window.addEventListener("resize", resize);
  window.addEventListener(
    "pointerdown",
    () => {
      if (state.soundOn) audio.play(state.weather, state.intensity);
    },
    { once: true }
  );

  let lastTime = performance.now();
  function tick(now) {
    const dt = Math.min((now - lastTime) / 1000, 0.033);
    lastTime = now;

    ctx.clearRect(0, 0, state.width, state.height);
    updateParticles(dt);
    updateSunScene(dt);

    requestAnimationFrame(tick);
  }

  resize();
  syncLabels();
  onWeatherChange();
  requestAnimationFrame(tick);
})();
