"use client";

import { useEffect, useState } from "react";

type Language = "en" | "es";

const repositoryUrl = "https://github.com/EduardoRemedios/factory-starter-kit";

const copy = {
  en: {
    nav: {
      model: "The model",
      process: "How it works",
      pod: "The pod",
      install: "Try Factory",
    },
    hero: {
      eyebrow: "Open-source AI delivery system",
      title: "AI builds the software.",
      titleAccent: "Humans set the direction and stay in control.",
      body: "Factory is the operating system for teams where AI is the principal designer, architect, developer, tester, reviewer, documenter and evidence producer—not merely a coding assistant.",
      human:
        "People own the vision, business constraints, consequential decisions, execution approval, accountability and final acceptance.",
      primary: "See how it works",
      secondary: "View on GitHub",
      proof: ["Open source", "Codex + Claude", "Human-approved execution"],
    },
    model: {
      kicker: "A different operating model",
      title: "Not a copilot. A delivery principal.",
      intro:
        "A copilot waits for a developer to drive every step. Factory gives capable AI a governed route through the full software lifecycle.",
      oldLabel: "Copilot model",
      oldTitle: "Human production, AI assistance",
      old: [
        "Humans author the design and code",
        "AI helps one task at a time",
        "Quality depends on continuous human supervision",
        "Process knowledge lives with individuals",
      ],
      newLabel: "Factory model",
      newTitle: "Human intent, AI production",
      modern: [
        "Humans lock the outcome and boundaries",
        "AI designs, builds, tests and documents",
        "Independent challenge and gates test the work",
        "Evidence travels with every delivery",
      ],
    },
    process: {
      kicker: "Governed from idea to evidence",
      title: "Speed without skipping the thinking.",
      intro:
        "Factory turns a business intent into an auditable execution pack before code changes begin.",
      steps: [
        ["01", "Intent", "Lock the outcome, constraints, non-goals and acceptance criteria."],
        ["02", "Challenge", "Red and Blue responsibilities expose weak assumptions and harden the brief."],
        ["03", "Risk", "Pre-mortem the failure modes before they become expensive."],
        ["04", "Verification", "Design fixtures and proof before implementation."],
        ["05", "Human Go", "A person reviews the pack and authorizes execution."],
        ["06", "Execute", "AI completes bounded micro-sprints in a fixed sequence."],
        ["07", "Prove", "Purple adjudication and deterministic checks close the evidence chain."],
      ],
    },
    boundary: {
      kicker: "Authority stays human",
      title: "Autonomous technical delivery does not mean autonomous business control.",
      humanTitle: "Humans remain accountable for",
      human: [
        "Product vision and priorities",
        "Business, legal and risk constraints",
        "Consequential decisions",
        "Execution authorization",
        "Final acceptance",
      ],
      aiTitle: "AI is principal for",
      ai: [
        "Solution design and architecture",
        "Implementation and integration",
        "Testing and regression evidence",
        "Review and documentation",
        "Delivery closeout",
      ],
    },
    pod: {
      kicker: "Small by design",
      title: "A modern delivery pod: three people, many AI specialist lanes.",
      intro:
        "Factory replaces a large role map with a compact human control system around an AI delivery principal.",
      roles: [
        {
          number: "01",
          title: "Product / Domain Owner",
          text: "Owns the problem, desired outcome, domain truth and final acceptance.",
        },
        {
          number: "02",
          title: "AI Delivery Director",
          text: "Directs Factory runs, translates intent into executable work and keeps delivery moving.",
        },
        {
          number: "03",
          title: "Assurance & Risk Partner",
          text: "Challenges assumptions, checks evidence and protects independent judgment.",
        },
      ],
      engineTitle: "The AI delivery engine",
      engine:
        "Architecture · Development · Testing · Review · Documentation · Evidence",
      variantTitle: "Two-person variant",
      variant:
        "For lower-risk work, delivery direction and assurance can be covered by two people—but independent challenge must still be preserved.",
    },
    adoption: {
      kicker: "Adopt without a rewrite",
      title: "Bring governance to the repository you already have.",
      intro:
        "The plugin carries Factory’s operating logic. A safe, preview-first setup then adds the project-local contracts and evidence structure your repository needs.",
      cards: [
        ["Diagnose", "A read-only doctor reports compatibility, prerequisites and the next legal action."],
        ["Preview", "Greenfield or brownfield setup produces an exact plan before writing anything."],
        ["Approve", "Repository changes require an explicit, plan-specific human approval."],
        ["Operate", "The same Factory Core works through Codex and Claude with namespaced commands."],
      ],
      note:
        "The plugin is the distribution layer. The project scaffold is the durable contract that travels with the code.",
    },
    install: {
      kicker: "Release candidate · v0.1.0-rc.1",
      title: "Install once. Start with Doctor.",
      intro:
        "Choose your environment. Factory diagnoses the repository before it recommends greenfield or brownfield setup.",
      codex: "ChatGPT / Codex desktop",
      claude: "Claude Code",
      copy: "Copy",
      copied: "Copied",
      detail: "Full installation and update instructions live in the public repository.",
      repo: "Open installation guide",
    },
    faq: {
      kicker: "Straight answers",
      title: "What engineering teams usually ask.",
      items: [
        [
          "Is Factory another coding assistant?",
          "No. Coding assistants help a developer produce work. Factory governs an AI-principal delivery process from locked intent through planning, execution and inspectable evidence.",
        ],
        [
          "Does the plugin replace project setup?",
          "No. The plugin distributes Factory’s commands and skills. Each repository still receives a previewed, explicitly approved project scaffold so its rules and evidence stay with the code.",
        ],
        [
          "Does Factory replace product thinking?",
          "No. Vision, research, business intent, non-functional requirements and constraints can be prepared upstream. Factory turns an authorized brief into governed technical delivery.",
        ],
        [
          "Are testing and regression covered?",
          "Yes. Verification is designed before implementation, project-native tests remain authoritative, and completion requires recorded evidence rather than a confidence claim.",
        ],
        [
          "Do Red, Blue and Purple require different AI models?",
          "No. They are independent responsibilities in the process. The selected session model can serve all three unless a team intentionally configures separate routing.",
        ],
        [
          "Is Factory ready for every risk level?",
          "The current release is a public release candidate. Teams should start with bounded pilots, keep human approval gates, and add project-specific security, compliance and merge controls where required.",
        ],
      ],
    },
    close: {
      label: "The operating model for AI-principal software delivery",
      title: "Give AI the work. Keep humans in control.",
      body: "Start with the public release candidate, test it in a bounded repository and inspect the evidence for yourself.",
      cta: "Explore Factory on GitHub",
    },
    footer: {
      by: "Factory was designed by Eduardo A dos Remedios.",
      license: "Open source · Apache-2.0",
      top: "Back to top",
    },
  },
  es: {
    nav: {
      model: "El modelo",
      process: "Cómo funciona",
      pod: "El equipo",
      install: "Probar Factory",
    },
    hero: {
      eyebrow: "Sistema de entrega con IA de código abierto",
      title: "La IA construye el software.",
      titleAccent: "Las personas marcan la dirección y mantienen el control.",
      body: "Factory es el sistema operativo para equipos en los que la IA es la principal diseñadora, arquitecta, desarrolladora, probadora, revisora, documentalista y productora de evidencias; no es simplemente un asistente de programación.",
      human:
        "Las personas son responsables de la visión, las restricciones del negocio, las decisiones importantes, la autorización de la ejecución, la rendición de cuentas y la aceptación final.",
      primary: "Ver cómo funciona",
      secondary: "Ver en GitHub",
      proof: ["Código abierto", "Codex + Claude", "Ejecución aprobada por personas"],
    },
    model: {
      kicker: "Un modelo operativo diferente",
      title: "No es un copiloto. Es el principal responsable de la entrega.",
      intro:
        "Un copiloto espera a que un desarrollador dirija cada paso. Factory ofrece a una IA capaz una ruta gobernada a través de todo el ciclo de vida del software.",
      oldLabel: "Modelo copiloto",
      oldTitle: "Producción humana, asistencia de IA",
      old: [
        "Las personas redactan el diseño y el código",
        "La IA ayuda en una tarea cada vez",
        "La calidad depende de supervisión humana continua",
        "El conocimiento del proceso reside en individuos",
      ],
      newLabel: "Modelo Factory",
      newTitle: "Intención humana, producción de IA",
      modern: [
        "Las personas fijan el resultado y los límites",
        "La IA diseña, construye, prueba y documenta",
        "El desafío independiente y las puertas de control comprueban el trabajo",
        "La evidencia acompaña cada entrega",
      ],
    },
    process: {
      kicker: "Gobernado desde la idea hasta la evidencia",
      title: "Velocidad sin saltarse el razonamiento.",
      intro:
        "Factory transforma una intención de negocio en un paquete de ejecución auditable antes de que empiecen los cambios de código.",
      steps: [
        ["01", "Intención", "Fija el resultado, las restricciones, lo que no se hará y los criterios de aceptación."],
        ["02", "Desafío", "Las responsabilidades Roja y Azul revelan supuestos débiles y refuerzan el encargo."],
        ["03", "Riesgo", "Anticipa los fallos antes de que resulten costosos."],
        ["04", "Verificación", "Diseña ejemplos de referencia y pruebas antes de implementar."],
        ["05", "Aprobación humana", "Una persona revisa el paquete y autoriza la ejecución."],
        ["06", "Ejecución", "La IA completa micro-sprints acotados en una secuencia fija."],
        ["07", "Evidencia", "La revisión Púrpura y las comprobaciones deterministas cierran la cadena de pruebas."],
      ],
    },
    boundary: {
      kicker: "La autoridad sigue siendo humana",
      title: "La entrega técnica autónoma no significa control empresarial autónomo.",
      humanTitle: "Las personas siguen siendo responsables de",
      human: [
        "Visión y prioridades del producto",
        "Restricciones empresariales, legales y de riesgo",
        "Decisiones importantes",
        "Autorización de la ejecución",
        "Aceptación final",
      ],
      aiTitle: "La IA es principal en",
      ai: [
        "Diseño de la solución y arquitectura",
        "Implementación e integración",
        "Pruebas y evidencia de regresión",
        "Revisión y documentación",
        "Cierre de la entrega",
      ],
    },
    pod: {
      kicker: "Pequeño por diseño",
      title: "Un equipo de entrega moderno: tres personas y muchas especialidades de IA.",
      intro:
        "Factory sustituye un mapa enorme de roles por un sistema compacto de control humano alrededor de un principal de entrega de IA.",
      roles: [
        {
          number: "01",
          title: "Responsable de Producto / Dominio",
          text: "Es responsable del problema, el resultado deseado, la verdad del dominio y la aceptación final.",
        },
        {
          number: "02",
          title: "Director de Entrega con IA",
          text: "Dirige las ejecuciones de Factory, convierte la intención en trabajo ejecutable y mantiene el avance.",
        },
        {
          number: "03",
          title: "Socio de Garantía y Riesgo",
          text: "Cuestiona supuestos, comprueba evidencias y protege el juicio independiente.",
        },
      ],
      engineTitle: "El motor de entrega de IA",
      engine:
        "Arquitectura · Desarrollo · Pruebas · Revisión · Documentación · Evidencia",
      variantTitle: "Variante de dos personas",
      variant:
        "Para trabajos de menor riesgo, la dirección de entrega y la garantía pueden cubrirse con dos personas, pero debe conservarse el desafío independiente.",
    },
    adoption: {
      kicker: "Adopción sin reescribir",
      title: "Añade gobernanza al repositorio que ya tienes.",
      intro:
        "El plugin transporta la lógica operativa de Factory. Después, una configuración segura y con vista previa añade los contratos locales y la estructura de evidencias que necesita el repositorio.",
      cards: [
        ["Diagnosticar", "Un doctor de solo lectura informa de compatibilidad, requisitos previos y la siguiente acción legal."],
        ["Previsualizar", "La configuración nueva o existente produce un plan exacto antes de escribir nada."],
        ["Aprobar", "Los cambios del repositorio requieren una aprobación humana explícita y específica del plan."],
        ["Operar", "El mismo Factory Core funciona mediante Codex y Claude con comandos separados por espacio de nombres."],
      ],
      note:
        "El plugin es la capa de distribución. La estructura del proyecto es el contrato duradero que viaja con el código.",
    },
    install: {
      kicker: "Versión candidata · v0.1.0-rc.1",
      title: "Instala una vez. Empieza con Doctor.",
      intro:
        "Elige tu entorno. Factory diagnostica el repositorio antes de recomendar una configuración nueva o para un proyecto existente.",
      codex: "Escritorio ChatGPT / Codex",
      claude: "Claude Code",
      copy: "Copiar",
      copied: "Copiado",
      detail: "Las instrucciones completas de instalación y actualización están en el repositorio público.",
      repo: "Abrir guía de instalación",
    },
    faq: {
      kicker: "Respuestas directas",
      title: "Lo que suelen preguntar los equipos de ingeniería.",
      items: [
        [
          "¿Factory es otro asistente de programación?",
          "No. Los asistentes ayudan a un desarrollador a producir trabajo. Factory gobierna un proceso de entrega donde la IA es principal, desde la intención fijada hasta la planificación, la ejecución y la evidencia inspeccionable.",
        ],
        [
          "¿El plugin sustituye la configuración del proyecto?",
          "No. El plugin distribuye los comandos y capacidades de Factory. Cada repositorio recibe una estructura previsualizada y aprobada explícitamente para que sus reglas y evidencias permanezcan con el código.",
        ],
        [
          "¿Factory sustituye el pensamiento de producto?",
          "No. La visión, la investigación, la intención de negocio, los requisitos no funcionales y las restricciones pueden prepararse antes. Factory convierte un encargo autorizado en entrega técnica gobernada.",
        ],
        [
          "¿Incluye pruebas y regresión?",
          "Sí. La verificación se diseña antes de implementar, las pruebas propias del proyecto siguen siendo la autoridad y la finalización exige evidencias registradas, no una afirmación de confianza.",
        ],
        [
          "¿Rojo, Azul y Púrpura necesitan modelos de IA diferentes?",
          "No. Son responsabilidades independientes dentro del proceso. El modelo seleccionado para la sesión puede cumplir las tres, salvo que un equipo configure deliberadamente un enrutamiento separado.",
        ],
        [
          "¿Factory está listo para todos los niveles de riesgo?",
          "La versión actual es una candidata pública. Los equipos deben empezar con pilotos acotados, conservar las aprobaciones humanas y añadir controles específicos de seguridad, cumplimiento e integración cuando sean necesarios.",
        ],
      ],
    },
    close: {
      label: "El modelo operativo para la entrega de software con IA como principal",
      title: "Dale el trabajo a la IA. Mantén el control humano.",
      body: "Empieza con la versión candidata pública, pruébala en un repositorio acotado e inspecciona tú mismo las evidencias.",
      cta: "Explorar Factory en GitHub",
    },
    footer: {
      by: "Factory fue diseñado por Eduardo A dos Remedios.",
      license: "Código abierto · Apache-2.0",
      top: "Volver arriba",
    },
  },
} as const;

const installCommands = {
  codex: `/Applications/ChatGPT.app/Contents/Resources/codex \\
  plugin marketplace add EduardoRemedios/factory-starter-kit \\
  --ref factory-plugin-v0.1.0-rc.1

/Applications/ChatGPT.app/Contents/Resources/codex \\
  plugin add factory@factory-starter-kit

# In a new Codex task:
$factory-doctor`,
  claude: `claude plugin marketplace add \\
  EduardoRemedios/factory-starter-kit@factory-plugin-v0.1.0-rc.1

claude plugin install factory@factory-starter-kit --scope user

# In Claude Code:
/reload-plugins
/factory:doctor`,
};

function CheckList({ items }: { items: readonly string[] }) {
  return (
    <ul className="check-list">
      {items.map((item) => (
        <li key={item}>
          <span aria-hidden="true">↗</span>
          {item}
        </li>
      ))}
    </ul>
  );
}

export function FactorySite({ initialLanguage }: { initialLanguage: Language }) {
  const [language, setLanguage] = useState<Language>(initialLanguage);
  const [installTab, setInstallTab] = useState<"codex" | "claude">("codex");
  const [copied, setCopied] = useState(false);
  const text = copy[language];

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  function switchLanguage(next: Language) {
    setLanguage(next);
    const url = new URL(window.location.href);
    url.searchParams.set("lang", next);
    window.history.replaceState({}, "", url);
  }

  async function copyCommand() {
    await navigator.clipboard.writeText(installCommands[installTab]);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  return (
    <main id="top">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Factory home">
          <span className="brand-mark" aria-hidden="true">
            F<span>:</span>
          </span>
          <span>Factory</span>
        </a>
        <nav aria-label={language === "en" ? "Main navigation" : "Navegación principal"}>
          <a href="#model">{text.nav.model}</a>
          <a href="#process">{text.nav.process}</a>
          <a href="#pod">{text.nav.pod}</a>
          <a className="nav-cta" href="#install">
            {text.nav.install}
          </a>
        </nav>
        <div className="language-switch" aria-label="Language">
          <button
            type="button"
            className={language === "en" ? "active" : ""}
            aria-pressed={language === "en"}
            onClick={() => switchLanguage("en")}
          >
            EN
          </button>
          <span>/</span>
          <button
            type="button"
            className={language === "es" ? "active" : ""}
            aria-pressed={language === "es"}
            onClick={() => switchLanguage("es")}
          >
            ES
          </button>
        </div>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">
            <span className="status-dot" />
            {text.hero.eyebrow}
          </p>
          <h1>
            {text.hero.title}
            <span>{text.hero.titleAccent}</span>
          </h1>
          <p className="hero-body">{text.hero.body}</p>
          <p className="human-boundary">{text.hero.human}</p>
          <div className="hero-actions">
            <a className="button button-primary" href="#process">
              {text.hero.primary} <span aria-hidden="true">↓</span>
            </a>
            <a
              className="button button-secondary"
              href={repositoryUrl}
              target="_blank"
              rel="noreferrer"
            >
              {text.hero.secondary} <span aria-hidden="true">↗</span>
            </a>
          </div>
          <ul className="proof-row" aria-label="Product facts">
            {text.hero.proof.map((item) => (
              <li key={item}>
                <span aria-hidden="true">✓</span>
                {item}
              </li>
            ))}
          </ul>
        </div>
        <div className="delivery-map" aria-label={language === "en" ? "Factory delivery map" : "Mapa de entrega de Factory"}>
          <div className="map-grid" aria-hidden="true" />
          <div className="map-label map-label-human">
            <span>01</span>
            <strong>{language === "en" ? "HUMAN INTENT" : "INTENCIÓN HUMANA"}</strong>
            <small>{language === "en" ? "Direction + constraints" : "Dirección + límites"}</small>
          </div>
          <div className="map-rail" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
          <div className="map-core">
            <span className="core-ring" aria-hidden="true" />
            <strong>FACTORY</strong>
            <small>{language === "en" ? "AI delivery principal" : "Principal de entrega IA"}</small>
          </div>
          <div className="map-output">
            {["DESIGN", "BUILD", "TEST", "PROVE"].map((label, index) => (
              <span key={label}>
                <small>0{index + 2}</small>
                {language === "es"
                  ? ["DISEÑAR", "CREAR", "PROBAR", "DEMOSTRAR"][index]
                  : label}
              </span>
            ))}
          </div>
          <div className="map-label map-label-go">
            <span>GO</span>
            <strong>{language === "en" ? "HUMAN ACCEPTANCE" : "ACEPTACIÓN HUMANA"}</strong>
          </div>
        </div>
      </section>

      <section className="section model-section" id="model">
        <div className="section-heading">
          <p className="kicker">{text.model.kicker}</p>
          <h2>{text.model.title}</h2>
          <p>{text.model.intro}</p>
        </div>
        <div className="compare-grid">
          <article className="compare-card muted">
            <p className="card-label">{text.model.oldLabel}</p>
            <h3>{text.model.oldTitle}</h3>
            <CheckList items={text.model.old} />
          </article>
          <div className="shift" aria-hidden="true">
            <span>→</span>
          </div>
          <article className="compare-card bright">
            <p className="card-label">{text.model.newLabel}</p>
            <h3>{text.model.newTitle}</h3>
            <CheckList items={text.model.modern} />
          </article>
        </div>
      </section>

      <section className="section process-section" id="process">
        <div className="section-heading split">
          <div>
            <p className="kicker">{text.process.kicker}</p>
            <h2>{text.process.title}</h2>
          </div>
          <p>{text.process.intro}</p>
        </div>
        <ol className="process-list">
          {text.process.steps.map(([number, title, body]) => (
            <li key={number}>
              <span className="step-number">{number}</span>
              <h3>{title}</h3>
              <p>{body}</p>
              <span className="step-line" aria-hidden="true" />
            </li>
          ))}
        </ol>
      </section>

      <section className="boundary-section">
        <div className="section-heading boundary-heading">
          <p className="kicker">{text.boundary.kicker}</p>
          <h2>{text.boundary.title}</h2>
        </div>
        <div className="boundary-grid">
          <article className="boundary-card human-card">
            <div className="boundary-icon" aria-hidden="true">H</div>
            <h3>{text.boundary.humanTitle}</h3>
            <CheckList items={text.boundary.human} />
          </article>
          <article className="boundary-card ai-card">
            <div className="boundary-icon" aria-hidden="true">AI</div>
            <h3>{text.boundary.aiTitle}</h3>
            <CheckList items={text.boundary.ai} />
          </article>
        </div>
      </section>

      <section className="section pod-section" id="pod">
        <div className="section-heading">
          <p className="kicker">{text.pod.kicker}</p>
          <h2>{text.pod.title}</h2>
          <p>{text.pod.intro}</p>
        </div>
        <div className="pod-visual">
          <div className="role-grid">
            {text.pod.roles.map((role) => (
              <article className="role-card" key={role.number}>
                <span>{role.number}</span>
                <div className="role-avatar" aria-hidden="true">
                  <span />
                </div>
                <h3>{role.title}</h3>
                <p>{role.text}</p>
              </article>
            ))}
          </div>
          <div className="engine">
            <p>{text.pod.engineTitle}</p>
            <div className="engine-track" aria-hidden="true">
              <span />
              <strong>F:</strong>
              <span />
            </div>
            <strong>{text.pod.engine}</strong>
          </div>
        </div>
        <aside className="variant-note">
          <span>2</span>
          <div>
            <h3>{text.pod.variantTitle}</h3>
            <p>{text.pod.variant}</p>
          </div>
        </aside>
      </section>

      <section className="section adoption-section">
        <div className="section-heading split">
          <div>
            <p className="kicker">{text.adoption.kicker}</p>
            <h2>{text.adoption.title}</h2>
          </div>
          <p>{text.adoption.intro}</p>
        </div>
        <div className="adoption-grid">
          {text.adoption.cards.map(([title, body], index) => (
            <article key={title}>
              <span>0{index + 1}</span>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
        <p className="adoption-note">
          <span aria-hidden="true">i</span>
          {text.adoption.note}
        </p>
      </section>

      <section className="install-section" id="install">
        <div className="section-heading">
          <p className="kicker">{text.install.kicker}</p>
          <h2>{text.install.title}</h2>
          <p>{text.install.intro}</p>
        </div>
        <div className="terminal">
          <div className="terminal-top">
            <div className="install-tabs" role="tablist" aria-label="Installation environment">
              <button
                type="button"
                role="tab"
                aria-selected={installTab === "codex"}
                onClick={() => setInstallTab("codex")}
              >
                {text.install.codex}
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={installTab === "claude"}
                onClick={() => setInstallTab("claude")}
              >
                {text.install.claude}
              </button>
            </div>
            <button className="copy-button" type="button" onClick={copyCommand}>
              {copied ? text.install.copied : text.install.copy}
            </button>
          </div>
          <pre>
            <code>{installCommands[installTab]}</code>
          </pre>
        </div>
        <div className="install-detail">
          <p>{text.install.detail}</p>
          <a href={`${repositoryUrl}#install-the-plugin`} target="_blank" rel="noreferrer">
            {text.install.repo} <span aria-hidden="true">↗</span>
          </a>
        </div>
      </section>

      <section className="section faq-section">
        <div className="section-heading">
          <p className="kicker">{text.faq.kicker}</p>
          <h2>{text.faq.title}</h2>
        </div>
        <div className="faq-list">
          {text.faq.items.map(([question, answer], index) => (
            <details key={question} open={index === 0}>
              <summary>
                <span>{question}</span>
                <span aria-hidden="true">+</span>
              </summary>
              <p>{answer}</p>
            </details>
          ))}
        </div>
      </section>

      <section className="close-section">
        <p>{text.close.label}</p>
        <h2>{text.close.title}</h2>
        <div>
          <p>{text.close.body}</p>
          <a className="button close-button" href={repositoryUrl} target="_blank" rel="noreferrer">
            {text.close.cta} <span aria-hidden="true">↗</span>
          </a>
        </div>
      </section>

      <footer>
        <a className="brand" href="#top" aria-label="Factory home">
          <span className="brand-mark" aria-hidden="true">F<span>:</span></span>
          <span>Factory</span>
        </a>
        <p>{text.footer.by}</p>
        <p>{text.footer.license}</p>
        <a href="#top">{text.footer.top} ↑</a>
      </footer>
    </main>
  );
}
