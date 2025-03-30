import { useState, useEffect } from 'react';
import CCSizeContext from './CCSizeContext';
import { isMobile } from 'react-device-detect';

const CCSizeState = (props) => {
	const [CCSize, setCCSize] = useState(0.5);

	const medDevice = window.matchMedia(
		'(min-width: 1024px) and (max-width: 1366px)'
	);

	const lgDevice = window.matchMedia(
		'(min-width: 1367px) and (max-width: 1600px)'
	);

	const xlDevice = window.matchMedia('(min-width: 1601px)');

	useEffect(() => {
		const handleMediaQueryChange = (event) => {
			if (medDevice.matches) {
				setCCSize(0.65);
			} else if (lgDevice.matches) {
				setCCSize(0.7);
			} else if (xlDevice.matches) {
				setCCSize(0.8);
			}

			// Handle mobile notice
			if (isMobile && !sessionStorage.getItem('mobileAlertShown')) {
				// Set the flag first to prevent multiple instances
				sessionStorage.setItem('mobileAlertShown', 'true');

				// Create modal HTML directly
				const modalHTML = `
					<div id="mobile-modal-alert" style="position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0,0,0,0.85); z-index:9999; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:20px; color:white; font-family:sans-serif; text-align:center;">
						<div style="font-size:24px; font-weight:bold; margin-bottom:15px; color:#915EFF;">
							✨ Desktop Magic Ahead! ✨
						</div>
						<div>
							<p style="font-size:18px; margin-bottom:20px; line-height:1.5;">
								Hey there! You're missing the <span style="color:#915EFF; font-weight:bold;">MAGIC</span>!
								This portfolio has mind-blowing 3D effects that just don't fit on tiny screens.
							</p>
							<p style="font-size:16px; margin-bottom:20px; line-height:1.5;">
								Grab a laptop or desktop to see <span style="color:#915EFF; font-weight:bold;">floating tech icons</span>,
								<span style="color:#915EFF; font-weight:bold;">spinning worlds</span>, and
								<span style="color:#915EFF; font-weight:bold;">dancing 3D elements</span>!
							</p>
						</div>
						<button id="close-modal-btn" style="background-color:#915EFF; border:none; color:white; padding:12px 20px; border-radius:5px; font-size:16px; cursor:pointer; margin-top:15px; font-weight:bold;">
							I'll Check It Out Later
						</button>
					</div>
				`;

				// Insert the modal HTML
				document.body.insertAdjacentHTML('beforeend', modalHTML);

				// Add click event listener to the button
				setTimeout(() => {
					const closeBtn = document.getElementById('close-modal-btn');
					if (closeBtn) {
						closeBtn.onclick = function() {
							const modal = document.getElementById('mobile-modal-alert');
							if (modal) modal.remove();
						};
					}
				}, 100); // Small delay to ensure DOM is ready
			}
		};

		handleMediaQueryChange();

		// Add the callback function as a listener for changes to the media query
		medDevice.addEventListener('change', handleMediaQueryChange);
		lgDevice.addEventListener('change', handleMediaQueryChange);
		xlDevice.addEventListener('change', handleMediaQueryChange);

		// Remove the listener when the component is unmounted
		return () => {
			medDevice.removeEventListener('change', handleMediaQueryChange);
			lgDevice.removeEventListener('change', handleMediaQueryChange);
			xlDevice.removeEventListener('change', handleMediaQueryChange);
		};
	}, []);

	return (
		<>
			<CCSizeContext.Provider value={{ CCSize }}>
				{props.children}
			</CCSizeContext.Provider>
		</>
	);
};

export default CCSizeState;
