import { motion } from 'framer-motion';
import { styles } from '../styles';
import { staggerContainer } from '../utils/motion';
import { isMobile } from 'react-device-detect';

const SectionWrapper = (Component, idName) =>
	function HOC() {
		return (
			<motion.section
				variants={staggerContainer()}
				initial="hidden"
				whileInView="show"
				viewport={
					isMobile ? { once: true, amount: 0 } : { once: true, amount: 0.25 }
				}
				className={`${styles.padding} max-w-7xl mx-auto relative z-0`}>
				<span className="hash-span" id={idName}></span>
				<Component />
			</motion.section>
		);
	};

export default SectionWrapper;
