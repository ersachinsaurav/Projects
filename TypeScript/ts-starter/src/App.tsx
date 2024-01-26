import React from 'react';
import './App.css';
import Greet from './components/Greet';
import Person from './components/Person';
import PersonList from './components/PersonList';
import Status from './components/Status';
import Heading from './components/Heading';
import Oscar from './components/Oscar';
import Button from './components/Button';
import Input from './components/Input';
import Container from './components/Container';
import Counter from './components/states/Counter';
import { ThemeContextProvider } from './components/contexts/ThemeContext';
import Box from './components/contexts/Box';
import { UserContextProvider } from './components/contexts/UserContext';
import { User } from './components/contexts/User';
import { DomRef } from './components/refs/DomRef';
import { MutableRef } from './components/refs/MutableRef';
import { CCounter } from './components/classes/Counter';
import Private from './components/auth/Private';
import Profile from './components/auth/Profile';
import List from './components/generics/List';
import { RandomNumber } from './components/restrictions/RandomNumber';
import Toast from './components/templateLiterals/Toast';
import CustomButton from './components/htmls/CustomButton';
import Text from './components/polymorphics/Text';

function App() {
  const person = {
    firstName: 'Sachin',
    lastName: 'Saurav',
  };

  const personList = [
    { firstName: 'Bruce', lastName: 'Wayne' },
    { firstName: 'Clark', lastName: 'Kent' },
    { firstName: 'Princess', lastName: 'Diana' },
  ];

  return (
    <div className="App">
      <Greet name={'Sachin'} isLoggedIn={true} />
      <Greet name={'Saurav'} messageCount={20} isLoggedIn={true} />
      <Person name={person} />
      <PersonList names={personList} />
      <Status status={'loading'} />
      <Heading>Placeholder Text</Heading>
      <Oscar>
        <Heading>Oscar goes to Sachin Saurav!</Heading>
      </Oscar>
      <Button
        handleClick={(event, id) => {
          console.log('Clicked', event, id);
        }}
      ></Button>
      <Input
        value={''}
        handleChange={(event) => {
          console.log(event);
        }}
      />
      <Container styles={{ border: '1px solid red', padding: '1rem' }} />
      <Counter />
      <ThemeContextProvider>
        <Box />
      </ThemeContextProvider>
      <UserContextProvider>
        <User />
      </UserContextProvider>
      <DomRef />
      <MutableRef />

      <CCounter message={'The count value is'} />

      <Private isLoggedIn={true} component={Profile} />
      {/* <List
        items={['Batman', 'Superman', 'Wonder Woman']}
        onClick={(item) => console.log(item)}
      />
      <List items={[1, 2, 3]} onClick={(item) => console.log(item)} /> */}
      <List
        items={[
          { id: 1, firstName: 'Sachin', lastName: 'Saurav' },
          { id: 2, firstName: 'Nitika', lastName: 'Saurav' },
        ]}
        onClick={(item) => console.log(item)}
      />
      <RandomNumber value={10} isPositive={true} />
      <Toast position={'center'} />
      <CustomButton
        variant="primary"
        onClick={() => {
          console.log('Primary Button Clicked');
        }}
      >
        Primary Button
      </CustomButton>

      <Text as="h1" size="lg">
        Heading
      </Text>
      <Text as="p" size="md">
        Paragraph
      </Text>
      <Text as="label" size="sm" color="secondary" htmlFor={'labelId'}>
        Label
      </Text>
    </div>
  );
}

export default App;
