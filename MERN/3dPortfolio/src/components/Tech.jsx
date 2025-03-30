import React from 'react';

import { BallCanvas } from './canvas';
import { SectionWrapper } from '../hoc';
import { technologies } from '../constants';
import { isMobile } from 'react-device-detect';
import { techCanvasLite } from '../assets';

const Tech = () => {
	return (
		<div className="flex flex-row flex-wrap justify-center gap-10">
			{isMobile && <img src={techCanvasLite} className="w-full h-auto" />}
			{!isMobile &&
				technologies.map((technology) => (
					<div className="w-28 h-28" key={technology.name}>
						<BallCanvas icon={technology.icon} />
						<p className="text-center text-white text-[14px] mt-2">{technology.name}</p>
					</div>
				))}
		</div>
	);
};

export default SectionWrapper(Tech, '');
