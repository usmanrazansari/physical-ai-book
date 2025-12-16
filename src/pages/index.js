import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Read the Book - 5 min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({ title, description, icon }) {
  return (
    <div className={`col col--4 ${styles.featureCard}`}>
      <div className={styles.featureCardInner}>
        <div className={styles.icon}>{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

function BookCard({ title, description, module }) {
  return (
    <div className={`col col--4 ${styles.bookCard}`}>
      <div className={clsx('card', styles.bookCardInner)}>
        <div className="card__body">
          <h3 className={styles.bookTitle}>{title}</h3>
          <span className={styles.moduleTag}>{module}</span>
          <p className={styles.bookDescription}>{description}</p>
        </div>
      </div>
    </div>
  );
}

function HomepageContent() {
  const [isVisible, setIsVisible] = useState({});

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          setIsVisible(prev => ({
            ...prev,
            [entry.target.id]: entry.isIntersecting
          }));
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    document.querySelectorAll('[data-animate]').forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const features = [
    {
      title: 'Physical AI Concepts',
      description: 'Learn about embodied intelligence and AI systems operating in the physical world.',
      icon: '📚'
    },
    {
      title: 'Humanoid Robotics',
      description: 'Explore the fascinating intersection of artificial intelligence and robotics.',
      icon: '🤖'
    },
    {
      title: 'Academic Approach',
      description: 'Rigorous academic content with theoretical foundations and principles.',
      icon: '🎓'
    }
  ];

  const books = [
    {
      title: 'The Robotic Nervous System',
      description: 'Foundational concepts of robot operating systems with ROS 2 architecture and Python agents.',
      module: 'Module 1'
    },
    {
      title: 'The Digital Twin',
      description: 'Simulation technologies for robotics using Gazebo physics and Unity digital twins.',
      module: 'Module 2'
    },
    {
      title: 'The AI-Robot Brain',
      description: 'AI integration and perception systems with NVIDIA Isaac and navigation technologies.',
      module: 'Module 3'
    }
  ];

  return (
    <main>
      {/* Features Section */}
      <section
        id="features"
        data-animate
        className={clsx(styles.features, isVisible.features ? styles.visible : '')}
      >
        <div className="container">
          <div className="row">
            {features.map((feature, index) => (
              <FeatureCard
                key={index}
                title={feature.title}
                description={feature.description}
                icon={feature.icon}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Featured Books Section */}
      <section
        id="books"
        data-animate
        className={clsx(styles.featuredBooks, isVisible.books ? styles.visible : '')}
      >
        <div className="container">
          <div className="text--center padding-horiz--md">
            <h2 className={styles.sectionTitle}>Featured Modules</h2>
            <p className={styles.sectionSubtitle}>Explore the comprehensive modules of Physical AI & Humanoid Robotics</p>
          </div>
          <div className="row">
            {books.map((book, index) => (
              <BookCard
                key={index}
                title={book.title}
                description={book.description}
                module={book.module}
              />
            ))}
            {/* Add the 4th book - Vision-Language-Action */}
            <div className={`col col--4 ${styles.bookCard}`}>
              <div className={clsx('card', styles.bookCardInner)}>
                <div className="card__body">
                  <h3 className={styles.bookTitle}>Vision-Language-Action (VLA)</h3>
                  <span className={styles.moduleTag}>Module 4</span>
                  <p className={styles.bookDescription}>Advanced human-robot interaction with voice-to-action systems and LLM planning for autonomous humanoid systems.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section
        id="cta"
        data-animate
        className={clsx(styles.cta, isVisible.cta ? styles.visible : '')}
      >
        <div className="container">
          <div className="text--center padding-horiz--md">
            <h2 className={styles.ctaTitle}>Ready to Dive In?</h2>
            <p className={styles.ctaSubtitle}>Start your journey into the world of Physical AI and humanoid robotics today.</p>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro">
              Begin Reading
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An educational book on embodied intelligence and AI systems operating in the physical world">
      <HomepageHeader />
      <HomepageContent />
    </Layout>
  );
}