const STATE_DATA={"100":{src:"assets/pbr/timer_100_pbr.glb",poster:"assets/hero_poster.png",radius:"50.000",area:"1.00",label:"100%"},"50":{src:"assets/pbr/timer_50_pbr.glb",poster:"assets/hero_poster.png",radius:"35.355",area:"0.50",label:"50%"},"10":{src:"assets/pbr/timer_10_pbr.glb",poster:"assets/hero_poster.png",radius:"15.811",area:"0.10",label:"10%"}};

const PART_DATA={housing:{title:"Upper housing",body:"外壳已有服务开口与主要外形关系。当前只证明模型存在这些结构；壁厚稳定性、boss、分型线、注塑方向和真实装配公差仍未验证。"},diffuser:{title:"Formed diffuser",body:"扩散件作为独立部件存在。材料牌号、热成形半径、厚度变化、光扩散均匀性和边缘亮度仍需实物光学样片。"},optical:{title:"Optical module",body:"三区光学隔舱、LED PCB 与 24 颗 LED envelope 已进入模型拓扑。真实光路、LED bin、驱动、电流、热耦合和热点控制均未验证。"},thermal:{title:"Heat spreader",body:"铝散热层是候选热路径。当前没有温升、热像、接触热阻或长时间运行数据，不得把金属片存在写成热性能通过。"},control:{title:"Control module",body:"XIAO RP2040 与 Bourns 编码器只按已核验 envelope 进入空间布置。最终 PCB、USB-C 电源架构、ESD、保护和旋钮触觉仍待工程化。"},service:{title:"Service closure",body:"底盖、脚圈和紧固件建立了可维护方向，但尚未证明重复拆装寿命、螺柱强度、密封、防滑或制造可行性。"}};

const stateModel=document.querySelector("#stateModel");
const stateCaption=document.querySelector("#stateCaption");
document.querySelectorAll(".state-button").forEach(button=>{button.addEventListener("click",()=>{const state=button.dataset.state;const data=STATE_DATA[state];document.querySelectorAll(".state-button").forEach(b=>{const active=b===button;b.classList.toggle("is-active",active);b.setAttribute("aria-pressed",String(active));});if(stateModel){stateModel.poster=data.poster;stateModel.src=data.src;stateModel.alt=`Timer Light Basin ${data.label} 剩余时间状态模型`;}if(stateCaption){stateCaption.innerHTML=`<strong>${data.label} / r = ${data.radius} mm</strong><span>A/A₁₀₀ = ${data.area} · DESIGN INPUT</span>`;}});});

const partDetail=document.querySelector("#partDetail");
document.querySelectorAll(".part-row").forEach(row=>{row.addEventListener("click",()=>{document.querySelectorAll(".part-row").forEach(r=>r.classList.toggle("is-active",r===row));const data=PART_DATA[row.dataset.part];partDetail.innerHTML=`<p class="kicker">STRUCTURE BOUNDARY</p><h3>${data.title}</h3><p>${data.body}</p>`;});});

document.querySelectorAll(".filter-button").forEach(button=>{button.addEventListener("click",()=>{const filter=button.dataset.filter;document.querySelectorAll(".filter-button").forEach(b=>{const active=b===button;b.classList.toggle("is-active",active);b.setAttribute("aria-pressed",String(active));});document.querySelectorAll(".evidence-row").forEach(row=>{row.hidden=filter!=="all"&&row.dataset.evidence!==filter;});});});

const navLinks=[...document.querySelectorAll(".site-nav a")];
const sections=navLinks.map(a=>document.querySelector(a.getAttribute("href"))).filter(Boolean);
if("IntersectionObserver" in window){const observer=new IntersectionObserver(entries=>{const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];if(!visible)return;navLinks.forEach(a=>{a.classList.toggle("is-current",a.getAttribute("href")===`#${visible.target.id}`);});},{rootMargin:"-25% 0px -60% 0px",threshold:[0,.15,.4,.7]});sections.forEach(section=>observer.observe(section));}

customElements.whenDefined("model-viewer").then(()=>{document.documentElement.classList.add("model-viewer-ready");}).catch(()=>{});
