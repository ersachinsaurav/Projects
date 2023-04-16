import { useState, useEffect } from 'react';
import CCSizeContext from './CCSizeContext';
import { isMobile } from 'react-device-detect';

const CCSizeState = (props) => {
	const [CCSize, setCCSize] = useState(0.65);
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
				setCCSize(0.75);
			} else if (xlDevice.matches) {
				setCCSize(0.85);
			}
			if (isMobile) {
				alert(
					'To fully enjoy and experience the 3D objects and features available on this page, we recommend accessing it through a laptop or desktop device.'
				);
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
