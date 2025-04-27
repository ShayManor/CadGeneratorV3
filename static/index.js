import * as THREE        from 'three';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.158.0/examples/jsm/controls/OrbitControls.js';
import { STLLoader }     from 'https://cdn.jsdelivr.net/npm/three@0.158.0/examples/jsm/loaders/STLLoader.js';

const form         = document.getElementById('cadForm');
const getModelForm = document.getElementById('getModelForm');
const submitBtn    = document.getElementById('submitBtn');
const loadBtn      = document.getElementById('loadBtn');
const viewerBox    = document.getElementById('viewerBox');
const modelTitle   = document.getElementById('modelTitle');
const downloadBtn  = document.getElementById('downloadBtn');
const canvas       = document.getElementById('stlCanvas');

let scene, camera, renderer, controls, loader, mesh, blobUrl;

function initThree() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x111111);

  // Lights
  const dl1 = new THREE.DirectionalLight(0xffffff, 1.5);
  dl1.position.set(50, 50, 50);
  scene.add(dl1);
  const al = new THREE.AmbientLight(0xffffff, 0.8);
  scene.add(al);

  // Camera
  camera = new THREE.PerspectiveCamera(
    45,
    canvas.clientWidth / canvas.clientHeight,
    0.1,
    2000
  );
  camera.position.set(0, 0, 100);
  camera.lookAt(0, 0, 0);

  // Renderer
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);

  // Controls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // Loader
  loader = new STLLoader();

  window.addEventListener('resize', () => {
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  });

  (function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  })();
}

function clearScene() {
  if (mesh) {
    scene.remove(mesh);
    mesh.geometry.dispose();
    mesh.material.dispose();
    mesh = null;
  }
  if (blobUrl) {
    URL.revokeObjectURL(blobUrl);
    blobUrl = null;
  }
}

function loadSTL(url) {
  loader.load(url, geometry => {
    mesh = new THREE.Mesh(
      geometry,
      new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.3, roughness: 0.6 })
    );
    geometry.center();
    const size = new THREE.Box3().setFromObject(mesh).getSize(new THREE.Vector3()).length();
    mesh.scale.setScalar(50 / size);
    scene.add(mesh);
  });
}

async function handleFetch(url, formData, modelName) {
  submitBtn.disabled = loadBtn.disabled = true;
  clearScene();

  try {
    const res = await fetch(url, { method: 'POST', body: formData });
    if (!res.ok) throw new Error(await res.text());
    const blob = await res.blob();
    blobUrl = URL.createObjectURL(blob);

    modelTitle.textContent = modelName;
    viewerBox.hidden = false;

    if (!scene) initThree();
    loadSTL(blobUrl);

    downloadBtn.disabled = false;
    downloadBtn.onclick = () => {
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `${modelName}.stl`;
      a.click();
    };
  } catch (err) {
    alert(`Error: ${err.message}`);
  } finally {
    submitBtn.disabled = loadBtn.disabled = false;
  }
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const prompt = document.getElementById('prompt').value.trim();
  const name   = document.getElementById('name').value.trim();
  const iters  = +document.getElementById('iterations').value || 1;
  if (!prompt || !name) return;

  const fd = new FormData();
  fd.append('prompt', prompt);
  fd.append('name', name);
  fd.append('iterations', iters);

  handleFetch('/create_model', fd, name);
});

getModelForm.addEventListener('submit', e => {
  e.preventDefault();
  const name = document.getElementById('getModelName').value.trim();
  if (!name) return alert('Please enter a model name');

  const fd = new FormData();
  fd.append('name', name);

  handleFetch('/get_model', fd, name);
});
