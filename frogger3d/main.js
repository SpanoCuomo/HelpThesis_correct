let scene, camera, renderer;
let frog, lanes = [];
let cars = [];
const laneCount = 3;
const laneWidth = 5;
const carSpeed = 0.1;
const carFrequency = 100; // frames between new car spawn
let frame = 0;

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
    const frogGeometry = new THREE.BoxGeometry(1, 1, 1);
    const frogMaterial = new THREE.MeshPhongMaterial({color: 0x00ff00});
    frog = new THREE.Mesh(frogGeometry, frogMaterial);
    frog.position.set(0, 0.5, laneWidth * (laneCount / 2));
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
    const carGeometry = new THREE.BoxGeometry(2, 1, laneWidth - 1);
    const carMaterial = new THREE.MeshPhongMaterial({color: 0xff0000});
    const car = new THREE.Mesh(carGeometry, carMaterial);
    car.position.y = 0.5;
    car.position.z = lane.z;
    car.position.x = lane.direction === 1 ? -laneWidth * 2.5 : laneWidth * 2.5;
    car.userData = { direction: lane.direction };
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
    frog.position.set(0, 0.5, laneWidth * (laneCount / 2));
}

init();
