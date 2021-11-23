import NexusCard from "../../../../../core/components/nexusCard";
import {card} from "./style";

interface Props {
    description: string,
    tags: string[]
}

const SnippetCard = (props: Props) => {
    return (
        <div style={card}>
            <NexusCard>
                <p>{props.description}</p>
                <ul>
                    {
                        props.tags.map((item, idx) => {
                            return <li key={idx+item}>{item}</li>
                        })
                    }
                </ul>
            </NexusCard>
        </div>
    );
}

export default SnippetCard;