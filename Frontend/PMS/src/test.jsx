function ListItem(props)
{
    return <li>{props.animal}</li>
}

function List(props)
{
    return(
        <ul>
            {props.animals.map((animal)=>{
                return animal.startsWith('L')? <ListItem key={animal} animal={animal}/>:null;
            })}
        </ul>
    );
}

function Greeting()
{
    const animals = ["Lion", "Cow", "Snake", "Lizard"];
    return(
        <div>
            <h1 className="text-3xl font-bold mb-2">Animals: </h1>
            <List animals={animals}/>
        </div>
    )
}
export default Greeting;