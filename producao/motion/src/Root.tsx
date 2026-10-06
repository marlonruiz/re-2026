import React from 'react';
import {Composition} from 'remotion';
import {Criativo} from './Criativo';
export const Root: React.FC = () => (
  <Composition id="Criativo" component={Criativo as any} width={1080} height={1920} fps={30} durationInFrames={300}
    defaultProps={{} as any} calculateMetadata={({props}: any) => ({durationInFrames: Math.ceil((props.duration || 10) * 30)})} />
);
