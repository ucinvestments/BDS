<script lang="ts">
  import "../app.css";
  import { fade } from "svelte/transition";
  import { dev } from "$app/environment";
  import { injectAnalytics } from "@vercel/analytics/sveltekit";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";

  injectAnalytics({ mode: dev ? "development" : "production" });

  let { children } = $props();

  const navLinks = [
    { href: "/", label: "Explorer", icon: "mdi:home" },
    { href: "/about", label: "About", icon: "mdi:information" },
    { href: "/contributing", label: "Contributing", icon: "mdi:account-plus" },
    { href: "/resources", label: "Resources", icon: "mdi:book-open-page-variant" },
    { href: "/stats", label: "Statistics", icon: "mdi:chart-bar" },
    {
      href: "https://github.com/ucinvestments/BDS",
      label: "GitHub",
      icon: "mdi:github",
      external: true,
    },
  ];

  const footerLinks = [
    { href: "/", label: "Explorer" },
    { href: "/about", label: "About" },
    { href: "/contributing", label: "Contributing" },
    { href: "/resources", label: "Resources" },
    { href: "/stats", label: "Statistics" },
    { href: "https://bdsmovement.net/", label: "BDS Movement", external: true },
  ];

  const cryptoAddresses = [
    { label: "ETH", address: "0x623c7559ddC51BAf15Cc81bf5bc13c0B0EA14c01" },
    {
      label: "XMR",
      address:
        "44bvXALNkxUgSkGChKQPnj79v6JwkeYEkGijgKyp2zRq3EiuL6oewAv5u2c7FN7jbN1z7uj1rrPfL77bbsJ3cC8U2ADFoTj",
    },
  ];
</script>

<Navbar appName="BDS Search" logoIcon="mdi:magnify" links={navLinks} />

<main in:fade={{ duration: 300 }}>
  {@render children?.()}
</main>

<Footer
  appName="BDS Search Platform"
  description="Transparency in corporate involvement in activities targeted by BDS campaigns."
  links={footerLinks}
  contactEmail="admin@ucinvestments.info"
  altContactEmail="admin@ucinvestments.info"
  {cryptoAddresses}
  copyrightHolder="BDS Search Platform"
/>

<style>
  :global(html) {
    scroll-behavior: smooth;
  }

  main {
    min-height: calc(100vh - 400px);
  }
</style>
