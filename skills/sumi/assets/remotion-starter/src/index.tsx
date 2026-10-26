import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
import {project,durationInFrames} from './project';
const Root=()=> <Composition id="Film" component={Film} width={project.width} height={project.height} fps={project.fps} durationInFrames={durationInFrames}/>;
registerRoot(Root);
