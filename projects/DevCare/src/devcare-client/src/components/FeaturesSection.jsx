const features = [
  {
    tag: 'TRIAGE',
    title: 'Risk scoring at intake',
    description:
      'Analyze symptoms and history quickly to highlight urgent cases and reduce queue pressure.',
  },
  {
    tag: 'MONITORING',
    title: 'Continuous patient summaries',
    description:
      'Track trends from vitals and notes, then surface concise summaries for each shift handoff.',
  },
  {
    tag: 'FOLLOW-UP',
    title: 'Care gap detection',
    description:
      'Flag missing tests, delayed follow-ups, and likely no-show risks before outcomes are affected.',
  },
]

function FeaturesSection() {
  return (
    <section id="features" className="site-container py-14 sm:py-16">
      <div className="mb-8 max-w-3xl">
        <p className="text-sm font-bold uppercase tracking-[0.16em] text-[var(--color-primary)]">
          Core Features
        </p>
        <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
          Generic blocks for your healthcare AI landing page
        </h2>
      </div>

      <div className="grid gap-5 md:grid-cols-3">
        {features.map((feature) => (
          <article
            key={feature.title}
            className="elevated-card rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6"
          >
            <p className="text-xs font-bold uppercase tracking-[0.13em] text-[var(--color-accent)]">
              {feature.tag}
            </p>
            <h3 className="mt-2 text-xl font-bold">{feature.title}</h3>
            <p className="mt-3 text-sm leading-6 text-[var(--color-text-muted)] sm:text-base">
              {feature.description}
            </p>
          </article>
        ))}
      </div>
    </section>
  )
}

export default FeaturesSection