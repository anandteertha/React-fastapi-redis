import { useState } from 'react';

function ListGroup() {
  let items: string[] = ["Tokyo", "Mumbai", "San Francisco", "Raleigh"];
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const getMessage = () => {
    return items.length === 0 && <p>No items found</p>;
  };

  return (
    <>
      <h1>List</h1>
      {getMessage()}
      <ul className="list-group">
        {items.map((item, index) => (
          <li
            key={item}
            className={
              selectedIndex === index
                ? "list-group-item active"
                : "list-group-item"
            }
            onClick={() => setSelectedIndex(index)}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
