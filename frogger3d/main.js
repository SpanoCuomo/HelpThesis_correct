let scene, camera, renderer;
let frog, lanes = [];
let cars = [];
const laneCount = 3;
const laneWidth = 5;
let carSpeed = 0.1;
const carFrequency = 100; // frames between new car spawn
let frame = 0;

let score = 0;
let lives = 3;
let level = 1;
let lastLane = laneCount; // used to detect crossings
let colorStage = 0;
let gameOver = false;

function showMessage(text) {
    const el = document.getElementById('message');
    if (!el) return;
    el.textContent = text;
    el.classList.remove('hidden');
    el.classList.add('show');
    setTimeout(() => {
        el.classList.add('hidden');
        el.classList.remove('show');
    }, 2000);
}

function jump() {
    frog.position.y = 0.5;
    setTimeout(() => {
        frog.position.y = 0;
    }, 150);
}

function updateHUD() {
    document.getElementById('score').textContent = `Punteggio: ${score}`;
    document.getElementById('lives').innerHTML = `Vite: ${'❤'.repeat(lives)}`;
    document.getElementById('level').textContent = `Livello: ${level}`;
}

function getLaneIndex(z) {
    return Math.round((laneWidth * (laneCount / 2) - z) / laneWidth);
}

function updateFrogColor() {
    const stage = Math.floor(score / 1000);
    if (stage > colorStage) {
        colorStage = stage;
        const color = new THREE.Color(Math.random(), Math.random(), Math.random());
        frog.traverse(obj => {
            if (obj.isMesh && obj.material && obj.material.color) {
                obj.material.color.set(color);
            }
        });
        carSpeed *= 1.005;
        showMessage('Colore rana cambiato');
    }
}

function createFrog() {
    const frogGroup = new THREE.Group();
    const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
    const eyeMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
    const pupilMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });

    const bodyGeom = new THREE.SphereGeometry(0.5, 16, 16);
    const body = new THREE.Mesh(bodyGeom, bodyMaterial);
    body.position.y = 0.5;
    frogGroup.add(body);

    const headGeom = new THREE.SphereGeometry(0.35, 16, 16);
    const head = new THREE.Mesh(headGeom, bodyMaterial);
    head.position.set(0, 0.75, 0.4);
    frogGroup.add(head);

    const legGeom = new THREE.BoxGeometry(0.2, 0.2, 0.4);
    const frontLeft = new THREE.Mesh(legGeom, bodyMaterial);
    frontLeft.position.set(-0.3, 0.2, 0.3);
    frogGroup.add(frontLeft);
    const frontRight = frontLeft.clone();
    frontRight.position.x = 0.3;
    frogGroup.add(frontRight);
    const backLeft = frontLeft.clone();
    backLeft.position.z = -0.3;
    frogGroup.add(backLeft);
    const backRight = frontRight.clone();
    backRight.position.z = -0.3;
    frogGroup.add(backRight);

    const eyeGeom = new THREE.SphereGeometry(0.1, 8, 8);
    const leftEye = new THREE.Mesh(eyeGeom, eyeMaterial);
    leftEye.position.set(-0.12, 0.9, 0.6);
    frogGroup.add(leftEye);
    const rightEye = leftEye.clone();
    rightEye.position.x = 0.12;
    frogGroup.add(rightEye);

    const pupilGeom = new THREE.SphereGeometry(0.05, 8, 8);
    const leftPupil = new THREE.Mesh(pupilGeom, pupilMaterial);
    leftPupil.position.set(-0.12, 0.9, 0.7);
    frogGroup.add(leftPupil);
    const rightPupil = leftPupil.clone();
    rightPupil.position.x = 0.12;
    frogGroup.add(rightPupil);

    return frogGroup;
}

function createCar(direction) {
    const carGroup = new THREE.Group();
    const randomColor = new THREE.Color(Math.random(), Math.random(), Math.random());
    const bodyMaterial = new THREE.MeshPhongMaterial({ color: randomColor });
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });

    const baseGeom = new THREE.BoxGeometry(3, 0.7, laneWidth - 1);
    const base = new THREE.Mesh(baseGeom, bodyMaterial);
    base.position.y = 0.6;
    carGroup.add(base);

    const cabinGeom = new THREE.BoxGeometry(1.5, 0.8, laneWidth - 2);
    const cabin = new THREE.Mesh(cabinGeom, bodyMaterial);
    cabin.position.set(-0.2, 1.1, 0);
    carGroup.add(cabin);

    const hoodGeom = new THREE.BoxGeometry(1.2, 0.4, laneWidth - 2);
    const hood = new THREE.Mesh(hoodGeom, bodyMaterial);
    hood.position.set(1, 1, 0);
    carGroup.add(hood);

    const wheelGeom = new THREE.CylinderGeometry(0.4, 0.4, 0.8, 16);
    const positions = [
        [-1.1, 0.4, 0.45],
        [1.1, 0.4, 0.45],
        [-1.1, 0.4, -0.45],
        [1.1, 0.4, -0.45]
    ];
    positions.forEach(([x, y, z]) => {
        const wheel = new THREE.Mesh(wheelGeom, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
        carGroup.add(wheel);
    });

    carGroup.rotation.y = Math.PI / 2; // rotate the car by 90°
    carGroup.userData = { direction };
    return carGroup;
}

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
    scene.add(light);

    // Ground
    const groundGeometry = new THREE.PlaneGeometry(laneWidth * 5, laneWidth * laneCount);
    const grassTex = new THREE.TextureLoader().load('https://threejs.org/examples/textures/terrain/grasslight-big.jpg');
    grassTex.wrapS = grassTex.wrapT = THREE.RepeatWrapping;
    grassTex.repeat.set(10, laneCount);
    const groundMaterial = new THREE.MeshPhongMaterial({ map: grassTex });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    scene.add(ground);

    // Frog
    frog = createFrog();
    frog.position.set(0, 0, laneWidth * (laneCount / 2));
    frog.rotation.y = 0;
    scene.add(frog);
    lastLane = getLaneIndex(frog.position.z);
    updateHUD();
    document.getElementById('game-over').classList.add('hidden');

    camera.position.set(0, 10, 10);
    camera.lookAt(0, 0, 0);

    // Create lanes
    for (let i = 0; i < laneCount; i++) {
        lanes.push({ z: (i - laneCount / 2 + 0.5) * laneWidth, direction: i % 2 === 0 ? 1 : -1 });
    }

    window.addEventListener('resize', onWindowResize, false);
    document.addEventListener('keydown', onKeyDown);

    animate();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function onKeyDown(event) {
    const key = event.code;
    let moved = false;
    const step = laneWidth / 2;
    if (key === 'ArrowUp') { frog.position.z -= step; moved = true; frog.rotation.y = Math.PI; }
    if (key === 'ArrowDown') { frog.position.z += step; moved = true; frog.rotation.y = 0; }
    if (key === 'ArrowLeft') { frog.position.x -= step; frog.rotation.y = Math.PI / 2; }
    if (key === 'ArrowRight') { frog.position.x += step; frog.rotation.y = -Math.PI / 2; }

    const maxX = laneWidth * 2;
    frog.position.x = Math.max(-maxX, Math.min(maxX, frog.position.x));

    if (moved) {
        jump();
        const laneIndex = getLaneIndex(frog.position.z);
        if (laneIndex > lastLane && laneIndex <= laneCount) {
            const pts = 10 * level;
            score += pts;
            showMessage(`+${pts} punti`);
            updateFrogColor();
        }
        lastLane = laneIndex;
        updateHUD();
    }
}

function spawnCar(lane) {
    const car = createCar(lane.direction);
    car.position.z = lane.z;
    car.position.x = lane.direction === 1 ? -laneWidth * 2.5 : laneWidth * 2.5;
    scene.add(car);
    cars.push(car);
}

function animate() {
    requestAnimationFrame(animate);

    if (gameOver) return;

    frame++;
    if (frame % carFrequency === 0) {
        const lane = lanes[Math.floor(Math.random() * laneCount)];
        spawnCar(lane);
    }

    cars.forEach(car => {
        car.position.x += car.userData.direction * carSpeed;
        if (Math.abs(car.position.x) > laneWidth * 3) {
            scene.remove(car);
        }
    });
    cars = cars.filter(car => Math.abs(car.position.x) <= laneWidth * 3);

    checkCollisions();

    renderer.render(scene, camera);
}

function checkCollisions() {
    if (frog.position.z >= laneWidth * (laneCount / 2)) return;
    const frogBox = new THREE.Box3().setFromObject(frog);
    let collided = false;
    cars.forEach(car => {
        if (collided) return;
        const carBox = new THREE.Box3().setFromObject(car);
        if (frogBox.intersectsBox(carBox)) {
            lives--;
            showMessage('Vita persa');
            updateHUD();
            if (lives <= 0) {
                document.getElementById('game-over').classList.remove('hidden');
                gameOver = true;
            }
            resetFrog();
            collided = true;
        }
    });

    if (frog.position.z < -laneWidth * (laneCount / 2)) {
        const pts = 20 * level;
        score += pts;
        level++;
        showMessage(`+${pts} punti`);
        if (level % 10 === 0) {
            lives++;
            showMessage('Vita guadagnata');
        }
        carSpeed += 0.02;
        updateFrogColor();
        updateHUD();
        resetFrog();
    }
}

function resetFrog() {
    frog.position.set(0, 0, laneWidth * (laneCount / 2));
    frog.rotation.y = 0;
    lastLane = getLaneIndex(frog.position.z);
}

init();
