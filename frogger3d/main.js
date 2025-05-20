let scene, camera, renderer;
let frog, lanes = [];
let cars = [];
const laneCount = 3;
const laneWidth = 5;
const carSpeed = 0.1;
const carFrequency = 100; // frames between new car spawn
let frame = 0;

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
    const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });

    const baseGeom = new THREE.BoxGeometry(2, 0.5, laneWidth - 1);
    const base = new THREE.Mesh(baseGeom, bodyMaterial);
    base.position.y = 0.5;
    carGroup.add(base);

    const topGeom = new THREE.BoxGeometry(1, 0.5, laneWidth - 2);
    const top = new THREE.Mesh(topGeom, bodyMaterial);
    top.position.set(0, 0.75, 0);
    carGroup.add(top);

    const wheelGeom = new THREE.CylinderGeometry(0.25, 0.25, 0.5, 16);
    const positions = [
        [-0.7, 0.25, 0.4],
        [0.7, 0.25, 0.4],
        [-0.7, 0.25, -0.4],
        [0.7, 0.25, -0.4]
    ];
    positions.forEach(([x, y, z]) => {
        const wheel = new THREE.Mesh(wheelGeom, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
        carGroup.add(wheel);
    });

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
    const groundMaterial = new THREE.MeshPhongMaterial({color: 0x222222});
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    scene.add(ground);

    // Frog
    frog = createFrog();
    frog.position.set(0, 0, laneWidth * (laneCount / 2));
    scene.add(frog);

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
    if (key === 'ArrowUp') frog.position.z -= laneWidth;
    if (key === 'ArrowDown') frog.position.z += laneWidth;
    if (key === 'ArrowLeft') frog.position.x -= laneWidth;
    if (key === 'ArrowRight') frog.position.x += laneWidth;
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
    const frogBox = new THREE.Box3().setFromObject(frog);
    cars.forEach(car => {
        const carBox = new THREE.Box3().setFromObject(car);
        if (frogBox.intersectsBox(carBox)) {
            resetFrog();
        }
    });

    if (frog.position.z < -laneWidth * (laneCount / 2)) {
        alert('Hai vinto!');
        resetFrog();
    }
}

function resetFrog() {
    frog.position.set(0, 0, laneWidth * (laneCount / 2));
}

init();
