import os
import socket
import time
from datetime import datetime
try:
    import redis  # type: ignore[import-not-found]
except ImportError:
    redis = None
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# ConfigMap & Environment Variables
APP_ENV = os.getenv("APP_ENV", "AWS-EKS-PRODUCTION")
WELCOME_MSG = os.getenv("WELCOME_MSG", "KOK-APP // KUBERNETES NEURAL COMMAND CENTER")
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
POD_NAME = os.getenv("HOSTNAME", socket.gethostname())
START_TIME = time.time()

r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
    socket_connect_timeout=2
) if redis else None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOK-APP // Sci-Fi DevOps Matrix</title>
    <style>
        :root {
            --bg-dark: #02060d;
            --panel-bg: rgba(4, 15, 30, 0.85);
            --neon-blue: #00f3ff;
            --deep-blue: #0066ff;
            --cyber-cyan: #0aff99;
            --text-main: #d0f0ff;
            --text-dim: #5c85a6;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Courier New', Courier, monospace; }
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            overflow-x: hidden;
            min-height: 100vh;
        }
        #matrix-canvas {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
            opacity: 0.25;
            pointer-events: none;
        }
        .container {
            position: relative;
            z-index: 2;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        /* Header & Top Right DevOps Engineer Badge */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--neon-blue);
            padding-bottom: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0, 243, 255, 0.15);
            flex-wrap: wrap;
            gap: 15px;
        }
        .brand h1 {
            font-size: 1.8rem;
            color: var(--neon-blue);
            text-shadow: 0 0 12px rgba(0, 243, 255, 0.8);
            letter-spacing: 2px;
        }
        .brand p { color: var(--text-dim); font-size: 0.85rem; margin-top: 4px; }

        .engineer-badge {
            background: linear-gradient(135deg, rgba(0, 102, 255, 0.25), rgba(0, 243, 255, 0.15));
            border: 1px solid var(--neon-blue);
            padding: 12px 20px;
            border-radius: 6px;
            cursor: pointer;
            text-align: right;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
            user-select: none;
        }
        .engineer-badge:hover {
            box-shadow: 0 0 25px rgba(0, 243, 255, 0.8);
            transform: translateY(-2px);
        }
        .engineer-role {
            font-size: 0.95rem;
            font-weight: bold;
            color: var(--neon-blue);
            letter-spacing: 1px;
        }
        .engineer-hint {
            font-size: 0.7rem;
            color: var(--text-dim);
            display: block;
            margin-top: 2px;
        }
        .engineer-name {
            display: none;
            font-size: 1.25rem;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 0 0 10px var(--neon-blue), 0 0 20px var(--deep-blue);
            margin-top: 6px;
            letter-spacing: 2px;
            animation: glitchReveal 0.4s ease forwards;
        }
        .engineer-badge.revealed .engineer-name { display: block; }
        .engineer-badge.revealed .engineer-hint { display: none; }

        @keyframes glitchReveal {
            0% { opacity: 0; transform: scale(0.9) skewX(15deg); }
            50% { opacity: 1; transform: scale(1.05) skewX(-10deg); }
            100% { opacity: 1; transform: scale(1) skewX(0deg); }
        }

        /* Live Telemetry HUD Bar */
        .hud-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .hud-box {
            background: var(--panel-bg);
            border: 1px solid rgba(0, 243, 255, 0.35);
            border-left: 4px solid var(--neon-blue);
            padding: 14px;
            border-radius: 4px;
        }
        .hud-label { font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; }
        .hud-val { font-size: 1.15rem; font-weight: bold; color: var(--neon-blue); margin-top: 5px; word-break: break-all; }

        /* Stack Grid */
        .section-title {
            color: var(--neon-blue);
            font-size: 1.1rem;
            margin-bottom: 15px;
            letter-spacing: 1.5px;
            border-left: 3px solid var(--deep-blue);
            padding-left: 10px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
            gap: 16px;
            margin-bottom: 25px;
        }
        .card {
            background: var(--panel-bg);
            border: 1px solid rgba(0, 102, 255, 0.4);
            border-radius: 6px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }
        .card:hover {
            border-color: var(--neon-blue);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.35);
            transform: translateY(-3px);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .card-title { font-weight: bold; color: #fff; font-size: 1rem; }
        .status-pill {
            font-size: 0.7rem;
            padding: 3px 8px;
            border-radius: 12px;
            background: rgba(0, 243, 255, 0.15);
            color: var(--neon-blue);
            border: 1px solid var(--neon-blue);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 4px rgba(0, 243, 255, 0.4); }
            50% { box-shadow: 0 0 12px rgba(0, 243, 255, 0.9); }
        }
        .card-desc { font-size: 0.82rem; color: var(--text-dim); line-height: 1.4; }
        .card-click { font-size: 0.72rem; color: var(--neon-blue); margin-top: 10px; display: block; }

        /* Live Terminal Feed */
        .terminal {
            background: rgba(1, 8, 18, 0.92);
            border: 1px solid var(--deep-blue);
            border-radius: 6px;
            padding: 15px;
            height: 180px;
            overflow-y: auto;
            font-size: 0.82rem;
        }
        .log-line { margin-bottom: 6px; color: #7ec8ff; }
        .log-time { color: var(--neon-blue); margin-right: 8px; }

        /* Algorithm Pop-Up Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 5, 15, 0.85);
            z-index: 100;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .modal-box {
            background: #031022;
            border: 2px solid var(--neon-blue);
            box-shadow: 0 0 35px rgba(0, 243, 255, 0.5);
            max-width: 650px;
            width: 100%;
            border-radius: 8px;
            padding: 25px;
            position: relative;
            animation: glitchReveal 0.25s ease;
        }
        .modal-close {
            position: absolute;
            top: 15px; right: 18px;
            background: none;
            border: 1px solid var(--neon-blue);
            color: var(--neon-blue);
            padding: 4px 10px;
            cursor: pointer;
            font-weight: bold;
        }
        .modal-title { color: var(--neon-blue); font-size: 1.3rem; margin-bottom: 12px; }
        .algo-steps {
            background: #010814;
            border-left: 3px solid var(--deep-blue);
            padding: 12px;
            margin: 12px 0;
            font-size: 0.85rem;
            line-height: 1.6;
            color: #bce6ff;
            white-space: pre-line;
        }

        /* Live Toast Pop-up */
        #toast-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .toast {
            background: rgba(2, 18, 38, 0.95);
            border: 1px solid var(--neon-blue);
            border-left: 4px solid var(--neon-blue);
            color: #fff;
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 0.8rem;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
            animation: glitchReveal 0.3s ease;
        }
    </style>
</head>
<body>
    <canvas id="matrix-canvas"></canvas>

    <div class="container">
        <header>
            <div class="brand">
                <h1>[ KOK-APP // MATRIX DEVOPS CORE ]</h1>
                <p id="welcome-banner">{{ welcome_msg }} | ENV: {{ app_env }}</p>
            </div>

            <!-- Interactive Right Corner DevOps Engineer Badge -->
            <div class="engineer-badge" id="engineer-badge" onclick="revealEngineer()">
                <div class="engineer-role">&lt;/&gt; DevOps Engineer</div>
                <span class="engineer-hint">[ CLICK TO DECRYPT IDENTITY ]</span>
                <div class="engineer-name">SALMAN KHAN</div>
            </div>
        </header>

        <!-- Real-Time Live Telemetry -->
        <div class="hud-bar">
            <div class="hud-box">
                <div class="hud-label">Active Serving Pod (Replica)</div>
                <div class="hud-val" id="hud-pod">{{ pod_name }}</div>
            </div>
            <div class="hud-box">
                <div class="hud-label">Redis Persistent Hits (PVC)</div>
                <div class="hud-val" id="hud-hits">SYNCING...</div>
            </div>
            <div class="hud-box">
                <div class="hud-label">Cluster Scheduling Mode</div>
                <div class="hud-val">TAINT + TOLERATION ACTIVE</div>
            </div>
            <div class="hud-box">
                <div class="hud-label">Pod Uptime & Health</div>
                <div class="hud-val" id="hud-uptime">0s [HEALTHY]</div>
            </div>
        </div>

        <div class="section-title">LIVE CLOUD-NATIVE ARCHITECTURE MATRIX (CLICK ANY MODULE TO INSPECT ALGORITHM)</div>
        <div class="grid" id="cards-grid"></div>

        <div class="section-title">LIVE KUBERNETES & CI/CD TELEMETRY STREAM</div>
        <div class="terminal" id="terminal-logs"></div>
    </div>

    <!-- Algorithm Inspection Modal -->
    <div class="modal-overlay" id="algo-modal" onclick="closeModal(event)">
        <div class="modal-box" onclick="event.stopPropagation()">
            <button class="modal-close" onclick="forceCloseModal()">X</button>
            <div class="modal-title" id="modal-title"></div>
            <div id="modal-subtitle" style="color: #5c85a6; font-size: 0.85rem;"></div>
            <div class="algo-steps" id="modal-algo"></div>
            <div style="font-size: 0.8rem; color: #00f3ff;" id="modal-impact"></div>
        </div>
    </div>

    <div id="toast-container"></div>

    <script>
        // 1. Matrix Cyber-Blue Falling Rain Animation
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const chars = '01KOKAPPEKSDOCKERK8STERRAFORM89ABCDEF';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function drawMatrix() {
            ctx.fillStyle = 'rgba(2, 6, 13, 0.08)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00f3ff';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 45);

        // 2. Top-Right Badge Click Handler -> Reveals Salman Khan
        function revealEngineer() {
            const badge = document.getElementById('engineer-badge');
            badge.classList.toggle('revealed');
            if (badge.classList.contains('revealed')) {
                showToast('IDENTITY VERIFIED: DevOps Engineer Salman Khan');
                addLog('AUTH // Identity decrypted: Salman Khan [Cluster Admin]');
            }
        }

        // 3. Architecture Modules & Live Algorithms
        const modules = [
            {
                name: 'Terraform IaC + AWS EKS',
                status: 'PROVISIONED',
                desc: 'VPC, Public Subnets, IAM Roles & EKS v1.31 Worker Nodes.',
                algo: '1. Parse HCL declarative state graph (main.tf, vpc.tf, ecr.tf)\\n2. Construct DAG (Directed Acyclic Graph) for resource dependencies\\n3. Provision VPC 10.0.0.0/16 -> Subnets -> EKS Control Plane -> t3.small Nodes\\n4. Configure EBS CSI Driver & OIDC/IAM cluster admin access.',
                impact: 'REAL-TIME RESULT: Automated immutable AWS cloud infrastructure in 12 mins.'
            },
            {
                name: 'GitHub Actions CI/CD + ECR',
                status: 'PIPELINE GREEN',
                desc: 'Automated build, security scan & push to Amazon ECR.',
                algo: '1. Trigger webhook on git push to main branch\\n2. Authenticate via AWS IAM credentials & login to ECR registry\\n3. Build multi-layer slim Docker container & tag with git commit SHA\\n4. Push image to ECR & execute kubectl rollout restart/apply.',
                impact: 'REAL-TIME RESULT: Zero-touch deployment from code commit to live EKS pod.'
            },
            {
                name: 'K8s Deployment & Replicas',
                status: '2/2 READY',
                desc: 'High availability with 2 load-balanced Flask pod replicas.',
                algo: '1. ReplicaSet controller continuously reconciles Desired State (2) == Current State\\n2. Round-robin/IPVS load balancing distributes HTTP hits across pods\\n3. RollingUpdate (maxSurge: 1, maxUnavailable: 0) ensures zero downtime.',
                impact: 'REAL-TIME RESULT: Refresh browser to watch Pod Hostname switch dynamically!'
            },
            {
                name: 'Taints & Tolerations',
                status: 'NODE ISOLATED',
                desc: 'Node 1 tainted (dedicated=db:NoSchedule) exclusively for Redis.',
                algo: '1. Kube-Scheduler filters nodes matching Pod Predicates\\n2. Node 1 rejects pods lacking key="dedicated", value="db", effect="NoSchedule"\\n3. App replicas forced onto Node 2; Redis pod matches Toleration & lands on Node 1.',
                impact: 'REAL-TIME RESULT: Database CPU/RAM protected from frontend traffic spikes.'
            },
            {
                name: 'Liveness & Readiness Probes',
                status: 'ACTIVE CHECKS',
                desc: 'Self-healing HTTP probes on /healthz and /ready endpoints.',
                algo: '1. Kubelet executes HTTP GET /ready every 5s -> verifies Redis ping()\\n2. If /ready fails (503), Endpoints controller removes Pod IP from Service\\n3. Kubelet executes HTTP GET /healthz every 10s -> restarts container on hang.',
                impact: 'REAL-TIME RESULT: 0% failed user requests during startup or DB hiccups.'
            },
            {
                name: 'PV, PVC & AWS EBS Storage',
                status: '2Gi BOUND',
                desc: 'Dynamic EBS volume attached to Redis for persistent state.',
                algo: '1. PVC requests 2Gi ReadWriteOnce from StorageClass gp2\\n2. AWS EBS CSI Driver dynamically provisions physical EBS disk in ap-south-1\\n3. Volume mounted at /data inside Redis container.',
                impact: 'REAL-TIME RESULT: Visitor counter survives Pod deletion & Rolling Updates.'
            },
            {
                name: 'ClusterIP, NodePort & Ingress',
                status: 'ROUTING LIVE',
                desc: 'Internal DB isolation + NGINX Ingress external routing.',
                algo: '1. Redis exposed ONLY via ClusterIP (internal DNS: redis-service:6379)\\n2. NGINX Ingress Controller listens on NodePort 30744 & routes / to kok-app-clusterip\\n3. Direct NodePort 30080 exposed for low-level debugging.',
                impact: 'REAL-TIME RESULT: Multi-tier network security with single entry gateway.'
            },
            {
                name: 'DaemonSet & Static Pod',
                status: 'NODE AGENTS',
                desc: 'Node-level monitoring DaemonSet + Kubelet Static Watchdog.',
                algo: '1. DaemonSet controller schedules 1 monitoring pod per eligible worker node\\n2. Static Pod manifest in /etc/kubernetes/manifests watched directly by Kubelet\\n3. Kubelet auto-restarts Static Pod even if K8s API server disconnects.',
                impact: 'REAL-TIME RESULT: Full node-level observability & control-plane resilience.'
            },
            {
                name: 'ConfigMap & Resource Limits',
                status: 'ENFORCED',
                desc: 'Decoupled env configs + CPU/Memory cgroup boundaries.',
                algo: '1. ConfigMap injects APP_ENV & WELCOME_MSG as container env variables\\n2. Linux cgroups enforce requests (100m CPU/128Mi) & limits (300m/256Mi)\\n3. OOMKiller terminates runaway containers before node crash.',
                impact: 'REAL-TIME RESULT: Zero noisy-neighbor crashes & dynamic config updates.'
            }
        ];

        const grid = document.getElementById('cards-grid');
        modules.forEach((m, idx) => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <div class="card-header">
                    <span class="card-title">${m.name}</span>
                    <span class="status-pill">${m.status}</span>
                </div>
                <div class="card-desc">${m.desc}</div>
                <span class="card-click">[ CLICK TO INSPECT ALGORITHM & WORKFLOW ]</span>
            `;
            card.onclick = () => openModal(m);
            grid.appendChild(card);
        });

        function openModal(m) {
            document.getElementById('modal-title').innerText = '// ' + m.name.toUpperCase();
            document.getElementById('modal-subtitle').innerText = 'STATUS: ' + m.status + ' | LIVE EXECUTION ALGORITHM';
            document.getElementById('modal-algo').innerText = m.algo;
            document.getElementById('modal-impact').innerText = m.impact;
            document.getElementById('algo-modal').style.display = 'flex';
            showToast('INSPECTING ALGORITHM: ' + m.name);
            addLog('ALGO-INSPECT // Viewed execution logic for [' + m.name + ']');
        }
        function closeModal(e) { if (e.target.id === 'algo-modal') forceCloseModal(); }
        function forceCloseModal() { document.getElementById('algo-modal').style.display = 'none'; }

        function showToast(msg) {
            const container = document.getElementById('toast-container');
            const t = document.createElement('div');
            t.className = 'toast';
            t.innerText = '> ' + msg;
            container.appendChild(t);
            setTimeout(() => t.remove(), 3500);
        }

        function addLog(text) {
            const term = document.getElementById('terminal-logs');
            const now = new Date().toLocaleTimeString();
            const line = document.createElement('div');
            line.className = 'log-line';
            line.innerHTML = `<span class="log-time">[${now}]</span> ${text}`;
            term.prepend(line);
        }

        // 4. Live Telemetry Polling from Kubernetes Backend
        let lastPod = '';
        async function fetchTelemetry() {
            try {
                const res = await fetch('/api/telemetry');
                const data = await res.json();
                document.getElementById('hud-pod').innerText = data.pod_name;
                document.getElementById('hud-hits').innerText = data.visitor_count + ' HITS';
                document.getElementById('hud-uptime').innerText = data.uptime_sec + 's [200 OK]';

                if (lastPod && lastPod !== data.pod_name) {
                    showToast('LOAD BALANCER SWITCHED POD: ' + data.pod_name);
                    addLog('K8S-SVC // Traffic routed to replica: ' + data.pod_name);
                }
                lastPod = data.pod_name;
                addLog(`PROBE-OK // Pod=${data.pod_name} | RedisHits=${data.visitor_count} | Readiness=200`);
            } catch (err) {
                addLog('WARN // Telemetry sync retrying...');
            }
        }

        addLog('SYSTEM // KOK-APP Matrix Core Initialized on AWS EKS...');
        fetchTelemetry();
        setInterval(fetchTelemetry, 3500);
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML_TEMPLATE,
        app_env=APP_ENV,
        welcome_msg=WELCOME_MSG,
        pod_name=POD_NAME
    )

@app.route("/api/telemetry")
def telemetry():
    try:
        hits = r.incr("page_hits") if r else 1
    except Exception as e:
        hits = f"ERR ({str(e)})"
    return jsonify({
        "app": "kok-app",
        "environment": APP_ENV,
        "message": WELCOME_MSG,
        "visitor_count": hits,
        "pod_name": POD_NAME,
        "uptime_sec": int(time.time() - START_TIME),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

# Liveness Probe endpoint
@app.route("/healthz")
def health():
    return jsonify({"status": "alive"}), 200

# Readiness Probe endpoint
@app.route("/ready")
def ready():
    try:
        if r:
            r.ping()
        return jsonify({"status": "ready"}), 200
    except Exception:
        return jsonify({"status": "not ready - db down"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)