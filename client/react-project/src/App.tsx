import { useState } from 'react';

import Alert from './components/Alert';
import Button from './components/Button';

function App() {
  // let items: string[] = ["Tokyo", "Mumbai", "San Francisco", "Raleigh"];
  // const handleSelectItem = (item: string) => {
  //   console.log(item);
  // };
  // return (
  //   <div>
  //     <ListGroup
  //       items={items}
  //       heading="Cities"
  //       onSelectItem={handleSelectItem}
  //     ></ListGroup>
  //   </div>
  // );

  const handleAlertDismiss = () => {
    console.log("alert was dismissed!");
    setIsAlertVisible(false);
  };

  const alertText = <strong>Holy guacamole!</strong>;

  const alertComponent = (
    <Alert onDismiss={handleAlertDismiss}>
      {alertText}. You should check in on some of those fields below
    </Alert>
  );
  const [isAlertVisible, setIsAlertVisible] = useState(false);
  return (
    <>
      {isAlertVisible && alertComponent}
      <Button
        color="danger"
        onClick={() => {
          setIsAlertVisible(true);
        }}
      >
        My Button
      </Button>
    </>
  );
}

export default App;
