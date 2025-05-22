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
let victories = 0;
let obstacles = [];
let obstacleGroups = 1; // number of obstacle groups per lane
let highScores = [];

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

function renderHighScores() {
    const container = document.getElementById('high-scores');
    if (!container) return;
    container.classList.remove('hidden');
    container.innerHTML = '<h3>High Scores</h3>';
    const list = document.createElement('ol');
    highScores.forEach(s => {
        const li = document.createElement('li');
        li.textContent = `${s.name}: ${s.score}`;
        list.appendChild(li);
    });
    container.appendChild(list);
}

function loadHighScores() {
    try {
        highScores = JSON.parse(localStorage.getItem('froggerHighScores')) || [];
    } catch (e) {
        highScores = [];
    }
    renderHighScores();
}

function saveHighScores() {
    localStorage.setItem('froggerHighScores', JSON.stringify(highScores));
}

function addHighScore(name, value) {
    highScores.push({ name, score: value });
    highScores.sort((a, b) => b.score - a.score);
    if (highScores.length > 5) highScores.length = 5;
    saveHighScores();
    renderHighScores();
}

function clearObstacles() {
    obstacles.forEach(o => scene.remove(o));
    obstacles = [];
}

function addObstacles() {
    clearObstacles();
    const material = new THREE.MeshPhongMaterial({ color: 0x8B4513 });

    // Compute z positions where no cars pass (between lanes)
    const walkwayPositions = [];
    for (let i = 1; i < laneCount; i++) { // skip start and goal rows
        walkwayPositions.push(laneWidth * (laneCount / 2) - i * laneWidth);
    }

    walkwayPositions.forEach(zPos => {
        for (let g = 0; g < obstacleGroups; g++) {
            const group = new THREE.Group();
            const groupSize = Math.floor(Math.random() * 3) + 1; // 1-3 poles
            for (let p = 0; p < groupSize; p++) {
                const geom = new THREE.BoxGeometry(0.5, 1, 0.5);
                const pole = new THREE.Mesh(geom, material);
                pole.position.set(p * 0.6, 0.5, 0);
                group.add(pole);
            }
            group.position.set((Math.random() - 0.5) * laneWidth * 3, 0, zPos);
            scene.add(group);
            obstacles.push(group);
        }
    });

    obstacleGroups++; // increase difficulty for next map change
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

    const baseGeom = new THREE.BoxGeometry(3.4, 0.7, laneWidth - 1);
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

    const wheelGeom = new THREE.CylinderGeometry(0.45, 0.45, 0.9, 32);
    const positions = [
        [-1.3, 0.4, 1.0],
        [1.3, 0.4, 1.0],
        [-1.3, 0.4, -1.0],
        [1.3, 0.4, -1.0]
    ];
    positions.forEach(([x, y, z]) => {
        const wheel = new THREE.Mesh(wheelGeom, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
        carGroup.add(wheel);
    });

    // Orient the car in the driving direction
    carGroup.rotation.y = direction === 1 ? 0 : Math.PI;
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
    frog.rotation.y = Math.PI; // face toward the goal initially
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

    loadHighScores();

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
    const step = laneWidth / 4; // jump distance reduced
    const prev = frog.position.clone();
    const prevRot = frog.rotation.y;
    if (key === 'ArrowUp') { frog.position.z -= step; moved = true; frog.rotation.y = Math.PI; }
    if (key === 'ArrowDown') { frog.position.z += step; moved = true; frog.rotation.y = 0; }
    if (key === 'ArrowLeft') { frog.position.x -= step; moved = true; frog.rotation.y = Math.PI / 2; }
    if (key === 'ArrowRight') { frog.position.x += step; moved = true; frog.rotation.y = -Math.PI / 2; }

    const maxX = laneWidth * 2;
    frog.position.x = Math.max(-maxX, Math.min(maxX, frog.position.x));

    if (moved) {
        const frogBox = new THREE.Box3().setFromObject(frog);
        for (const o of obstacles) {
            const box = new THREE.Box3().setFromObject(o);
            if (frogBox.intersectsBox(box)) {
                frog.position.copy(prev);
                frog.rotation.y = prevRot;
                return;
            }
        }
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
                const name = prompt('Inserisci il tuo nome');
                if (name) addHighScore(name, score);
            }
            resetFrog();
            collided = true;
        }
    });

    obstacles.forEach(o => {
        if (collided) return;
        const box = new THREE.Box3().setFromObject(o);
        if (frogBox.intersectsBox(box)) {
            collided = true;
            resetFrog();
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
        victories++;
        if (victories % 3 === 0) {
            addObstacles();
        }
        updateFrogColor();
        updateHUD();
        resetFrog();
    }
}

function resetFrog() {
    frog.position.set(0, 0, laneWidth * (laneCount / 2));
    frog.rotation.y = Math.PI; // face upward at start
    lastLane = getLaneIndex(frog.position.z);
}

init();
