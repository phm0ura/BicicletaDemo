from flask import Flask, render_template_string, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ============================================================
# DADOS DA LOJA — facilmente substituíveis por um banco SQL
# ============================================================
BIKES = [
    {
        "id": 1,
        "name": "Urban Pulse",
        "category": "Urbana",
        "price": 2499.90,
        "old_price": 2899.90,
        "rating": 4.9,
        "reviews": 128,
        "badge": "Mais vendida",
        "image": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1000&q=85",
        "description": "Leve, confortável e perfeita para deslocamentos urbanos.",
        "specs": ["Alumínio 6061", "21 velocidades", "Freios a disco", "Aros 700"],
    },
    {
        "id": 2,
        "name": "Trail X Pro",
        "category": "Mountain Bike",
        "price": 4299.90,
        "old_price": 4799.90,
        "rating": 4.8,
        "reviews": 94,
        "badge": "Oferta",
        "image": "https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&w=1000&q=85",
        "description": "Suspensão dianteira e geometria preparada para trilhas.",
        "specs": ["Alumínio 6061", "24 velocidades", "Freios hidráulicos", "Suspensão 120mm"],
    },
    {
        "id": 3,
        "name": "Road Carbon S",
        "category": "Speed",
        "price": 7999.90,
        "old_price": 8999.90,
        "rating": 5.0,
        "reviews": 61,
        "badge": "Performance",
        "image": "https://images.unsplash.com/photo-1502744688674-c619d1586c9e?auto=format&fit=crop&w=1000&q=85",
        "description": "Velocidade e eficiência para quem quer ir além.",
        "specs": ["Fibra de carbono", "22 velocidades", "Freios a disco", "Pneus 700x28"],
    },
    {
        "id": 4,
        "name": "City Flow",
        "category": "Urbana",
        "price": 3199.90,
        "old_price": 3499.90,
        "rating": 4.7,
        "reviews": 73,
        "badge": "Conforto",
        "image": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1000&q=85",
        "description": "Posição confortável e visual elegante para a cidade.",
        "specs": ["Alumínio", "18 velocidades", "Freio hidráulico", "Bagageiro integrado"],
    },
    {
        "id": 5,
        "name": "Kids Rocket",
        "category": "Infantil",
        "price": 899.90,
        "old_price": 1099.90,
        "rating": 4.9,
        "reviews": 41,
        "badge": "Família",
        "image": "https://images.unsplash.com/photo-1593764592116-bfb2a97c642a?auto=format&fit=crop&w=1000&q=85",
        "description": "Segura, resistente e divertida para os pequenos.",
        "specs": ["Aço reforçado", "7 velocidades", "Freio V-Brake", "Aro 20"],
    },
    {
        "id": 6,
        "name": "E-City 500",
        "category": "Elétrica",
        "price": 6999.90,
        "old_price": 7499.90,
        "rating": 4.9,
        "reviews": 87,
        "badge": "Elétrica",
        "image": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=1000&q=85",
        "description": "Assistência elétrica para transformar seus deslocamentos.",
        "specs": ["Motor 500W", "Bateria 48V", "Autonomia até 80km", "Display LCD"],
    },
]


def money(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


HTML = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VELOZ — Bicicletas & Mobilidade</title>

<style>
:root{
    --green:#1f9d68;
    --green-dark:#14734b;
    --lime:#c8f36b;
    --ink:#122019;
    --muted:#68756e;
    --cream:#f7f8f4;
    --white:#fff;
    --line:#e3e8e2;
    --orange:#f28b35;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
    margin:0;
    font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    color:var(--ink);
    background:var(--cream);
}
button,input,select{font:inherit}
button{cursor:pointer}
a{text-decoration:none;color:inherit}

.topbar{
    background:var(--ink);
    color:#e9f4ec;
    text-align:center;
    padding:9px 15px;
    font-size:12px;
    letter-spacing:.2px;
}
header{
    background:#fff;
    border-bottom:1px solid var(--line);
    position:sticky;
    top:0;
    z-index:20;
}
.nav{
    max-width:1220px;
    margin:auto;
    height:76px;
    padding:0 25px;
    display:flex;
    align-items:center;
    gap:35px;
}
.logo{
    font-size:25px;
    font-weight:950;
    letter-spacing:-1.5px;
}
.logo span{color:var(--green)}
.menu{
    display:flex;
    gap:24px;
    color:#536057;
    font-size:14px;
    flex:1;
}
.menu a:hover{color:var(--green)}
.nav-actions{display:flex;align-items:center;gap:10px}
.icon-btn{
    width:42px;height:42px;border:1px solid var(--line);background:#fff;border-radius:50%;
}
.cart-btn{
    border:0;background:var(--ink);color:#fff;border-radius:999px;
    padding:11px 16px;font-weight:800;
}
.hero{
    max-width:1220px;
    margin:auto;
    padding:38px 25px 20px;
}
.hero-box{
    min-height:475px;
    border-radius:30px;
    overflow:hidden;
    position:relative;
    display:flex;
    align-items:center;
    padding:65px;
    background:
      linear-gradient(90deg,rgba(7,30,20,.93) 0%,rgba(7,30,20,.72) 42%,rgba(7,30,20,.08) 78%),
      url("https://images.unsplash.com/photo-1502744688674-c619d1586c9e?auto=format&fit=crop&w=1800&q=90") center/cover;
}
.hero-content{max-width:610px;color:#fff}
.eyebrow{
    display:inline-block;
    padding:7px 11px;
    border-radius:999px;
    background:rgba(200,243,107,.15);
    border:1px solid rgba(200,243,107,.35);
    color:var(--lime);
    font-size:12px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1.2px;
}
.hero h1{
    font-size:clamp(42px,6vw,72px);
    line-height:.96;
    letter-spacing:-4px;
    margin:18px 0;
}
.hero h1 span{color:var(--lime)}
.hero p{
    color:#d7e3da;
    font-size:17px;
    line-height:1.6;
    max-width:510px;
}
.cta{
    display:inline-flex;
    margin-top:15px;
    padding:14px 20px;
    background:var(--lime);
    color:#17301f;
    border-radius:12px;
    font-weight:900;
    border:0;
}
.container{max-width:1220px;margin:auto;padding:50px 25px}
.section-head{
    display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:25px
}
.section-head h2{margin:0;font-size:32px;letter-spacing:-1.4px}
.section-head p{margin:7px 0 0;color:var(--muted)}
.filters{display:flex;gap:9px;flex-wrap:wrap}
.filter{
    border:1px solid var(--line);
    background:#fff;
    padding:9px 14px;
    border-radius:999px;
    color:#56635b;
}
.filter.active,.filter:hover{background:var(--ink);color:#fff;border-color:var(--ink)}

.grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
}
.product{
    background:#fff;
    border:1px solid var(--line);
    border-radius:19px;
    overflow:hidden;
    transition:.2s ease;
}
.product:hover{transform:translateY(-5px);box-shadow:0 18px 40px rgba(18,32,25,.09)}
.product-image{height:270px;position:relative;overflow:hidden;background:#e8eee8}
.product-image img{width:100%;height:100%;object-fit:cover;transition:.4s}
.product:hover img{transform:scale(1.04)}
.badge{
    position:absolute;top:14px;left:14px;
    background:#fff;padding:7px 10px;border-radius:8px;
    font-size:11px;font-weight:900;
}
.heart{
    position:absolute;top:12px;right:12px;
    width:38px;height:38px;border-radius:50%;border:0;background:#fff;
    box-shadow:0 5px 18px #0002;
}
.product-body{padding:19px}
.category{font-size:11px;text-transform:uppercase;color:var(--green);font-weight:900;letter-spacing:.8px}
.product h3{margin:7px 0 5px;font-size:19px}
.rating{font-size:13px;color:#7a6a20}
.rating span{color:#849087}
.price-row{display:flex;align-items:end;gap:9px;margin:16px 0 4px}
.price{font-size:23px;font-weight:950}
.old{text-decoration:line-through;color:#9ba39e;font-size:12px}
.buy{
    width:100%;border:0;background:var(--ink);color:#fff;
    padding:12px;border-radius:10px;font-weight:850;margin-top:12px
}
.buy:hover{background:var(--green)}

.benefits{
    display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
    background:var(--line);border:1px solid var(--line);border-radius:18px;overflow:hidden
}
.benefit{background:#fff;padding:24px}
.benefit-icon{font-size:24px}
.benefit strong{display:block;margin-top:10px}
.benefit p{font-size:13px;color:var(--muted);line-height:1.5;margin-bottom:0}

.banner{
    background:var(--ink);color:#fff;border-radius:24px;padding:42px;
    display:flex;align-items:center;justify-content:space-between;gap:30px;
}
.banner h2{font-size:35px;letter-spacing:-1.5px;margin:0 0 8px}
.banner p{color:#b9c9be;margin:0;max-width:600px}

.api-demo{
    margin-top:45px;
    background:#0d1a14;color:#dce9df;border-radius:22px;padding:25px;
}
.api-demo h3{margin-top:0}
.api-row{display:flex;gap:10px;align-items:center}
.api-method{color:var(--lime);font-weight:900;font-family:monospace}
.api-url{font-family:monospace;color:#b9cabd}
.api-result{
    margin-top:15px;padding:16px;border-radius:12px;
    background:#07100b;color:#9eb3a4;font:12px/1.7 Consolas,monospace;white-space:pre-wrap;
}
footer{background:#fff;border-top:1px solid var(--line);padding:35px 25px;color:var(--muted);text-align:center;font-size:13px}

.modal{
    display:none;position:fixed;inset:0;background:#0008;z-index:50;
    align-items:center;justify-content:center;padding:20px;
}
.modal.open{display:flex}
.modal-box{
    background:#fff;border-radius:22px;max-width:850px;width:100%;overflow:hidden;
    display:grid;grid-template-columns:1fr 1fr;position:relative
}
.modal-image{min-height:450px}.modal-image img{width:100%;height:100%;object-fit:cover}
.modal-info{padding:35px}.close{position:absolute;right:15px;top:15px;width:38px;height:38px;border:0;border-radius:50%;background:#fff}
.specs{padding-left:20px;color:var(--muted);line-height:1.9}

.cart{
    position:fixed;right:20px;bottom:20px;background:var(--green);color:#fff;
    padding:13px 17px;border-radius:999px;font-weight:900;box-shadow:0 12px 35px #14734b55;
    display:none;z-index:30
}
.toast{
    position:fixed;right:22px;top:100px;background:var(--ink);color:#fff;
    padding:14px 18px;border-radius:12px;display:none;z-index:70
}
@media(max-width:900px){
    .menu{display:none}
    .grid{grid-template-columns:1fr 1fr}
    .benefits{grid-template-columns:1fr 1fr}
    .hero-box{padding:40px 30px}
}
@media(max-width:620px){
    .grid,.modal-box{grid-template-columns:1fr}
    .product-image{height:230px}
    .modal-image{min-height:280px}
    .benefits{grid-template-columns:1fr}
    .banner{display:block;padding:30px}
}
</style>
</head>

<body>
<div class="topbar">🚚 Frete grátis acima de R$ 999 · 10% OFF no PIX · Compra 100% segura</div>

<header>
<nav class="nav">
    <div class="logo">VELOZ<span>.</span></div>
    <div class="menu">
        <a href="#bicicletas">Bicicletas</a>
        <a href="#beneficios">Por que a Veloz?</a>
        <a href="#oferta">Ofertas</a>
        <a href="#api">Tecnologia</a>
    </div>
    <div class="nav-actions">
        <button class="icon-btn" onclick="showToast('Busca demonstrativa')">⌕</button>
        <button class="cart-btn" onclick="showToast('Carrinho: '+cartCount+' item(ns)')">🛒 <span id="cartTop">0</span></button>
    </div>
</nav>
</header>

<main>
<section class="hero">
    <div class="hero-box">
        <div class="hero-content">
            <span class="eyebrow">Nova coleção 2026</span>
            <h1>Pedale mais.<br><span>Viva melhor.</span></h1>
            <p>Bicicletas pensadas para cidade, trilha, estrada e aventura. Escolha sua próxima experiência.</p>
            <a class="cta" href="#bicicletas">Explorar bicicletas →</a>
        </div>
    </div>
</section>

<section class="container" id="bicicletas">
    <div class="section-head">
        <div>
            <h2>Encontre sua bike</h2>
            <p>Modelos selecionados para cada tipo de pedal.</p>
        </div>
        <div class="filters">
            <button class="filter active" onclick="filterProducts('Todas',this)">Todas</button>
            <button class="filter" onclick="filterProducts('Urbana',this)">Urbana</button>
            <button class="filter" onclick="filterProducts('Mountain Bike',this)">MTB</button>
            <button class="filter" onclick="filterProducts('Speed',this)">Speed</button>
            <button class="filter" onclick="filterProducts('Elétrica',this)">Elétrica</button>
            <button class="filter" onclick="filterProducts('Infantil',this)">Infantil</button>
        </div>
    </div>

    <div class="grid" id="productGrid">
    {% for bike in bikes %}
        <article class="product" data-category="{{ bike.category }}">
            <div class="product-image">
                <img src="{{ bike.image }}" alt="{{ bike.name }}">
                <span class="badge">{{ bike.badge }}</span>
                <button class="heart" onclick="favorite(this)">♡</button>
            </div>
            <div class="product-body">
                <div class="category">{{ bike.category }}</div>
                <h3>{{ bike.name }}</h3>
                <div class="rating">★★★★★ <span>{{ bike.rating }} · {{ bike.reviews }} avaliações</span></div>
                <div class="price-row">
                    <div class="price">{{ money(bike.price) }}</div>
                    <div class="old">{{ money(bike.old_price) }}</div>
                </div>
                <button class="buy" onclick="openProduct({{ bike.id }})">Ver detalhes</button>
            </div>
        </article>
    {% endfor %}
    </div>
</section>

<section class="container" id="beneficios">
    <div class="benefits">
        <div class="benefit"><div class="benefit-icon">🚚</div><strong>Entrega rápida</strong><p>Envio para todo o Brasil com rastreamento.</p></div>
        <div class="benefit"><div class="benefit-icon">🛡️</div><strong>Garantia</strong><p>Produtos com garantia e suporte especializado.</p></div>
        <div class="benefit"><div class="benefit-icon">💳</div><strong>Pagamento flexível</strong><p>PIX, cartão e parcelamento em até 12x.</p></div>
        <div class="benefit"><div class="benefit-icon">🔧</div><strong>Montagem inclusa</strong><p>Sua bike chega pronta para o primeiro pedal.</p></div>
    </div>
</section>

<section class="container" id="oferta">
    <div class="banner">
        <div>
            <h2>Semana do Pedal</h2>
            <p>Descontos especiais em modelos selecionados. Uma ótima seção para conectar campanhas do seu e-commerce ao backend Flask.</p>
        </div>
        <button class="cta" onclick="showToast('Oferta aplicada à demonstração!')">Ver ofertas</button>
    </div>
</section>

<section class="container" id="api">
    <div class="section-head">
        <div>
            <h2>Flask por trás da loja</h2>
            <p>Uma demonstração do frontend conversando com uma API Python.</p>
        </div>
    </div>
    <div class="api-demo">
        <h3>Endpoint de catálogo</h3>
        <div class="api-row"><span class="api-method">GET</span><span class="api-url">/api/bikes</span></div>
        <div id="apiResult" class="api-result">Clique no botão para consultar o backend →</div>
        <button class="cta" onclick="callApi()" style="margin-top:12px">Executar API</button>
    </div>
</section>
</main>

<footer>
    <strong>VELOZ.</strong> · Demonstração de e-commerce construída com Python + Flask + Jinja + JavaScript<br>
    <span>Projeto demonstrativo — produtos e preços fictícios.</span>
</footer>

<div id="cartFloat" class="cart">🛒 <span id="cartFloatCount">0</span> item(ns) no carrinho</div>
<div id="toast" class="toast"></div>

<div id="modal" class="modal" onclick="if(event.target===this)closeModal()">
    <div class="modal-box">
        <button class="close" onclick="closeModal()">✕</button>
        <div class="modal-image"><img id="modalImg" src="" alt=""></div>
        <div class="modal-info">
            <div class="category" id="modalCategory"></div>
            <h2 id="modalName"></h2>
            <div class="rating" id="modalRating"></div>
            <p id="modalDescription" style="color:var(--muted);line-height:1.6"></p>
            <ul class="specs" id="modalSpecs"></ul>
            <div class="price" id="modalPrice"></div>
            <button class="buy" onclick="addToCart()">Adicionar ao carrinho</button>
        </div>
    </div>
</div>

<script>
let cartCount = 0;
let selectedBike = null;

const bikes = {{ bikes|tojson }};

function money(v){
    return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
}

function filterProducts(category, btn){
    document.querySelectorAll('.filter').forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.product').forEach(card=>{
        card.style.display = category === 'Todas' || card.dataset.category === category ? '' : 'none';
    });
}

function favorite(btn){
    btn.textContent = btn.textContent === '♡' ? '♥' : '♡';
    showToast(btn.textContent === '♥' ? 'Adicionado aos favoritos' : 'Removido dos favoritos');
}

function openProduct(id){
    selectedBike = bikes.find(x=>x.id===id);
    document.getElementById('modalImg').src = selectedBike.image;
    document.getElementById('modalCategory').textContent = selectedBike.category;
    document.getElementById('modalName').textContent = selectedBike.name;
    document.getElementById('modalRating').textContent = '★★★★★  '+selectedBike.rating+' · '+selectedBike.reviews+' avaliações';
    document.getElementById('modalDescription').textContent = selectedBike.description;
    document.getElementById('modalSpecs').innerHTML = selectedBike.specs.map(x=>'<li>'+x+'</li>').join('');
    document.getElementById('modalPrice').textContent = money(selectedBike.price);
    document.getElementById('modal').classList.add('open');
}

function closeModal(){
    document.getElementById('modal').classList.remove('open');
}

function addToCart(){
    cartCount++;
    document.getElementById('cartTop').textContent = cartCount;
    document.getElementById('cartFloatCount').textContent = cartCount;
    document.getElementById('cartFloat').style.display = 'block';
    closeModal();
    showToast(selectedBike.name+' foi adicionada ao carrinho');
}

async function callApi(){
    const box = document.getElementById('apiResult');
    box.textContent = 'Consultando Flask...';
    const response = await fetch('/api/bikes');
    const data = await response.json();
    box.textContent = JSON.stringify(data, null, 2);
}

function showToast(message){
    const t = document.getElementById('toast');
    t.textContent = '✓ '+message;
    t.style.display = 'block';
    setTimeout(()=>t.style.display='none',2200);
}
</script>
</body>
</html>
"""


@app.template_filter("money")
def money_filter(value):
    return money(value)


@app.route("/")
def home():
    return render_template_string(
        HTML,
        bikes=BIKES,
        money=money,
        year=datetime.now().year
    )


# API REST: catálogo
@app.route("/api/bikes")
def api_bikes():
    category = request.args.get("category")

    data = BIKES
    if category:
        data = [bike for bike in BIKES if bike["category"].lower() == category.lower()]

    return jsonify({
        "success": True,
        "total": len(data),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "items": data
    })


# API REST: produto individual
@app.route("/api/bikes/<int:bike_id>")
def api_bike(bike_id):
    bike = next((x for x in BIKES if x["id"] == bike_id), None)

    if not bike:
        return jsonify({"success": False, "error": "Bicicleta não encontrada"}), 404

    return jsonify({"success": True, "item": bike})


# Simulação de checkout
@app.route("/api/checkout", methods=["POST"])
def checkout():
    payload = request.get_json(silent=True) or {}

    return jsonify({
        "success": True,
        "message": "Pedido recebido com sucesso!",
        "order_id": f"VELOZ-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "items": payload.get("items", []),
        "next_step": "Integração com gateway de pagamento"
    })


# Health check — útil para servidores, Docker e monitoramento
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "veloz-store",
        "framework": "Flask"
    })


if __name__ == "__main__":
    app.run(debug=True)
