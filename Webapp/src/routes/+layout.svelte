<script>
	import '../app.css';
	import { dev } from '$app/environment';
	import { inject } from '@vercel/analytics';
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import Icon from '@iconify/svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let mobileMenuOpen = false;

	function toggleDonationInfo() {
		const donationInfo = document.getElementById('donationInfo');
		if (donationInfo) {
			donationInfo.style.display = donationInfo.style.display === 'none' ? 'block' : 'none';
		}
	}

	function toggleMobileMenu() {
		mobileMenuOpen = !mobileMenuOpen;
	}

	function closeMobileMenu() {
		mobileMenuOpen = false;
	}

	onMount(() => {
		if (browser) {
			// Initialize Vercel Analytics
			inject({ mode: dev ? 'development' : 'production' });
		}
	});
</script>

<nav class="navbar">
	<div class="nav-container">
		<a href="/" class="logo-link">
			<div class="logo">
				<Icon icon="mdi:chart-donut" class="logo-icon" />
				<span class="logo-text">BDS Search</span>
			</div>
		</a>

		<!-- Mobile menu toggle -->
		<button class="mobile-menu-toggle" on:click={toggleMobileMenu} aria-label="Toggle navigation menu">
			<Icon icon={mobileMenuOpen ? "mdi:close" : "mdi:menu"} class="mobile-menu-icon" />
		</button>

		<!-- Desktop navigation -->
		<div class="nav-links desktop-nav">
			<a href="/" class="nav-link" class:active={$page.url.pathname === '/'}>
				<Icon icon="mdi:home" class="nav-icon" />
				Explorer
			</a>
			<a href="/about" class="nav-link" class:active={$page.url.pathname === '/about'}>
				<Icon icon="mdi:information" class="nav-icon" />
				About
			</a>
			<a
				href="/contributing"
				class="nav-link"
				class:active={$page.url.pathname === '/contributing'}
			>
				<Icon icon="mdi:account-plus" class="nav-icon" />
				Contributing
			</a>
			<a href="/resources" class="nav-link" class:active={$page.url.pathname === '/resources'}>
				<Icon icon="mdi:book-open-page-variant" class="nav-icon" />
				Resources
			</a>
			<a href="/stats" class="nav-link" class:active={$page.url.pathname === '/stats'}>
				<Icon icon="mdi:chart-bar" class="nav-icon" />
				Statistics
			</a>
			<a
				href="https://github.com/TheArctesian/BDS-Search"
				target="_blank"
				rel="noopener noreferrer"
				class="nav-link external"
			>
				<Icon icon="mdi:github" class="nav-icon" />
				GitHub
				<Icon icon="mdi:open-in-new" class="external-icon" />
			</a>
		</div>

		<!-- Mobile navigation -->
		{#if mobileMenuOpen}
			<div class="mobile-nav" in:fade={{ duration: 200 }}>
				<a href="/" class="mobile-nav-link" class:active={$page.url.pathname === '/'} on:click={closeMobileMenu}>
					<Icon icon="mdi:home" class="nav-icon" />
					Explorer
				</a>
				<a href="/about" class="mobile-nav-link" class:active={$page.url.pathname === '/about'} on:click={closeMobileMenu}>
					<Icon icon="mdi:information" class="nav-icon" />
					About
				</a>
				<a
					href="/contributing"
					class="mobile-nav-link"
					class:active={$page.url.pathname === '/contributing'}
					on:click={closeMobileMenu}
				>
					<Icon icon="mdi:account-plus" class="nav-icon" />
					Contributing
				</a>
				<a href="/resources" class="mobile-nav-link" class:active={$page.url.pathname === '/resources'} on:click={closeMobileMenu}>
					<Icon icon="mdi:book-open-page-variant" class="nav-icon" />
					Resources
				</a>
				<a href="/stats" class="mobile-nav-link" class:active={$page.url.pathname === '/stats'} on:click={closeMobileMenu}>
					<Icon icon="mdi:chart-bar" class="nav-icon" />
					Statistics
				</a>
				<a
					href="https://github.com/TheArctesian/BDS-Search"
					target="_blank"
					rel="noopener noreferrer"
					class="mobile-nav-link external"
					on:click={closeMobileMenu}
				>
					<Icon icon="mdi:github" class="nav-icon" />
					GitHub
					<Icon icon="mdi:open-in-new" class="external-icon" />
				</a>
			</div>
		{/if}
	</div>
</nav>

<main in:fade={{ duration: 300 }}>
	<slot />
</main>

<footer class="footer">
	<div class="footer-content">
		<div class="footer-section">
			<h4 class="footer-title">BDS Search Platform</h4>
			<p class="footer-text">
				Transparency in corporate involvement in activities targeted by BDS campaigns.
			</p>
		</div>

		<div class="footer-section">
			<h4 class="footer-title">Quick Links</h4>
			<div class="footer-links">
				<a href="/" class="footer-link">Explorer</a>
				<a href="/about" class="footer-link">About</a>
				<a href="/contributing" class="footer-link">Contributing</a>
				<a href="/resources" class="footer-link">Resources</a>
				<a href="/stats" class="footer-link">Statistics</a>
				<a
					href="https://bdsmovement.net/"
					target="_blank"
					rel="noopener noreferrer"
					class="footer-link"
				>
					BDS Movement
					<Icon icon="mdi:open-in-new" class="footer-external" />
				</a>
			</div>
		</div>

		<div class="footer-section">
			<h4 class="footer-title">Contact</h4>
			<div class="footer-links">
				<a href="mailto:admin@ucinvestments.info" class="footer-link">Contact Admin</a>
				<a href="mailto:press@ucinvestments.info" class="footer-link">Submit Research</a>
				<a href="mailto:dev@ucinvestments.info" class="footer-link">Development</a>
			</div>
		</div>

		<div class="footer-section">
			<h4 class="footer-title">Support This Project</h4>
			<p class="footer-text">
				This project is self-funded by Stephen. Donations help cover hosting and API costs.
			</p>
			<div class="donation-links">
				<button class="donate-button" on:click={toggleDonationInfo}>
					<Icon icon="mdi:heart" class="donate-icon" />
					Donate
				</button>
				<div class="donation-info" id="donationInfo" style="display: none;">
					<div class="crypto-address">
						<strong>ETH:</strong>
						<code class="address">0x623c7559ddC51BAf15Cc81bf5bc13c0B0EA14c01</code>
					</div>
					<div class="crypto-address">
						<strong>XMR:</strong>
						<code class="address"
							>44bvXALNkxUgSkGChKQPnj79v6JwkeYEkGijgKyp2zRq3EiuL6oewAv5u2c7FN7jbN1z7uj1rrPfL77bbsJ3cC8U2ADFoTj</code
						>
					</div>
					<p class="alt-contact">
						Or contact <a href="mailto:admin@ucinvestments.info">admin</a> for alternatives.
					</p>
				</div>
			</div>
		</div>
	</div>

	<div class="footer-bottom">
		<p>
			&copy; 2025 BDS Search Platform. Created by <a
				href="https://stephenokita.com"
				target="_blank"
				rel="noopener noreferrer">Stephen Okita</a
			>. Educational purposes only.
		</p>
	</div>
</footer>

<style>
	:global(html) {
		scroll-behavior: smooth;
	}

	.navbar {
		position: sticky;
		top: 0;
		z-index: 100;
		background: rgba(255, 255, 255, 0.95);
		backdrop-filter: blur(20px);
		border-bottom: 1px solid var(--border);
		box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
	}

	.nav-container {
		position: relative;
		max-width: 1400px;
		margin: 0 auto;
		padding: 1rem 2rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.logo-link {
		text-decoration: none;
	}

	.logo {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		transition: transform 0.3s ease;
	}

	.logo:hover {
		transform: scale(1.05);
	}

	:global(.logo-icon) {
		font-size: 2rem;
		color: var(--founder);
	}

	.logo-text {
		font-family: 'Space Grotesk', sans-serif;
		font-size: 1.25rem;
		font-weight: 700;
		color: var(--pri);
		letter-spacing: -0.01em;
	}

	.nav-links {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	.nav-link {
		display: flex;
		align-items: center;
		gap: 0.375rem;
		padding: 0.625rem 1.25rem;
		color: var(--text-secondary);
		text-decoration: none;
		font-weight: 500;
		border-radius: 0.75rem;
		transition: all 0.2s ease;
		position: relative;
	}

	:global(.nav-icon) {
		font-size: 1.125rem;
	}

	.nav-link:hover {
		background: var(--bg-secondary);
		color: var(--pri);
		transform: translateY(-1px);
	}

	.nav-link.active {
		background: linear-gradient(135deg, var(--founder), var(--pri));
		color: white;
	}

	.nav-link.external {
		border: 2px solid var(--border);
	}

	:global(.external-icon) {
		font-size: 0.875rem;
		margin-left: -0.125rem;
	}

	/* Mobile menu toggle */
	.mobile-menu-toggle {
		display: none;
		background: none;
		border: none;
		color: var(--text-secondary);
		cursor: pointer;
		padding: 0.5rem;
		border-radius: 0.5rem;
		transition: all 0.2s ease;
	}

	.mobile-menu-toggle:hover {
		background: var(--bg-secondary);
		color: var(--pri);
	}

	:global(.mobile-menu-icon) {
		font-size: 1.5rem;
	}

	/* Mobile navigation */
	.mobile-nav {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: white;
		border-top: 1px solid var(--border);
		box-shadow: var(--shadow-lg);
		z-index: 50;
		padding: 1rem 0;
	}

	.mobile-nav-link {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.875rem 2rem;
		color: var(--text-secondary);
		text-decoration: none;
		font-weight: 500;
		transition: all 0.2s ease;
		border-left: 3px solid transparent;
	}

	.mobile-nav-link:hover {
		background: var(--bg-secondary);
		color: var(--pri);
		border-left-color: var(--founder);
	}

	.mobile-nav-link.active {
		background: linear-gradient(135deg, var(--founder), var(--pri));
		color: white;
		border-left-color: var(--sec);
	}

	.mobile-nav-link.external {
		border-top: 1px solid var(--border);
		margin-top: 0.5rem;
		padding-top: 1.25rem;
	}

	main {
		min-height: calc(100vh - 400px);
	}

	.footer {
		background: linear-gradient(180deg, var(--bg-secondary) 0%, white 100%);
		border-top: 1px solid var(--border);
		margin-top: 4rem;
		padding: 3rem 0 1.5rem;
	}

	.footer-content {
		max-width: 1400px;
		margin: 0 auto;
		padding: 0 2rem;
		display: grid;
		grid-template-columns: 2fr 1fr 1fr 1fr;
		gap: 2rem;
		margin-bottom: 2rem;
	}

	.footer-section {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.footer-title {
		font-family: 'Space Grotesk', sans-serif;
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--pri);
		margin: 0;
	}

	.footer-text {
		color: var(--text-secondary);
		line-height: 1.6;
		font-size: 0.925rem;
		margin: 0;
	}

	.footer-links {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.footer-link {
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		color: var(--text-secondary);
		text-decoration: none;
		font-size: 0.925rem;
		transition: all 0.2s ease;
		width: fit-content;
	}

	.footer-link:hover {
		color: var(--founder);
		transform: translateX(4px);
	}

	:global(.footer-external) {
		font-size: 0.75rem;
	}

	.footer-bottom {
		max-width: 1400px;
		margin: 0 auto;
		padding: 2rem 2rem 0;
		border-top: 1px solid var(--border);
		text-align: center;
	}

	.footer-bottom p {
		color: var(--text-secondary);
		font-size: 0.875rem;
		margin: 0;
	}

	.footer-bottom a {
		color: var(--founder);
		text-decoration: none;
		font-weight: 500;
	}

	.footer-bottom a:hover {
		color: var(--pri);
		text-decoration: underline;
	}

	@media (max-width: 768px) {
		.nav-container {
			position: relative;
			flex-direction: row;
			justify-content: space-between;
			align-items: center;
			gap: 0;
			padding: 1rem 1.5rem;
		}

		.desktop-nav {
			display: none;
		}

		.mobile-menu-toggle {
			display: flex;
		}

		.logo-text {
			font-size: 1.125rem;
		}

		.footer-content {
			grid-template-columns: 1fr;
			gap: 2rem;
			padding: 0 1.5rem;
		}

		.footer-section {
			text-align: center;
		}

		.footer-links {
			align-items: center;
		}
	}

	@media (max-width: 480px) {
		.nav-container {
			padding: 1rem;
		}

		.mobile-nav-link {
			padding: 1rem 1.5rem;
		}
	}
</style>
