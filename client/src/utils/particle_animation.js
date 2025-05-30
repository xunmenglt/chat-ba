const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
const width = window.innerWidth;
const height = window.innerHeight;

canvas.width = width;
canvas.height = height;

const particles = [];
const connections = [];
const particleCount = 300;
const particleSpeed = 1;
const particleSize = 2;
const maxDistance = 100;
const lightningColor = "#fff";

class Particle {
  constructor() {
    this.x = Math.random() * width;
    this.y = Math.random() * height;
    this.color = "#fff";
    this.angle = Math.random() * 360;
    this.speed = Math.random() * particleSpeed;
    this.opacity = Math.random() * 0.5 + 0.5;
  }

  update() {
    this.x += Math.cos(this.angle) * this.speed;
    this.y += Math.sin(this.angle) * this.speed;

    if (this.x < 0 || this.x > width || this.y < 0 || this.y > height) {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
    }
  }

  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, particleSize, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
    ctx.fill();
  }
}

function createParticles() {
  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }
}

function drawConnections() {
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < maxDistance) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = lightningColor;
        ctx.lineWidth = 0.2 * (1 - distance / maxDistance);
        ctx.stroke();
        ctx.closePath();
      }
    }
  }
}

function animate() {
  ctx.clearRect(0, 0, width, height);

  for (const particle of particles) {
    particle.update();
    particle.draw();
  }

  drawConnections();

  requestAnimationFrame(animate);
}

document.addEventListener("mousemove", (e) => {
  const mouseX = e.clientX;
  const mouseY = e.clientY;

  for (const particle of particles) {
    const dx = mouseX - particle.x;
    const dy = mouseY - particle.y;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance < maxDistance) {
      particle.angle = Math.atan2(dy, dx);
      particle.speed = 5;
    } else {
      particle.speed = Math.random() * particleSpeed;
    }
  }
});